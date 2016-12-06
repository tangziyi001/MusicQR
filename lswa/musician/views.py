from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from wsgiref.util import FileWrapper
from .models import Music, MusicQuery
from .models import Music, Download
from handle_file import handle_uploaded_file, find_ext 
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import os
import sys
import mimetypes
import hashlib
import pyqrcode
import time
import logging
import qrcode
import png
import json

sys.path.insert(0, '/home/ubuntu/LSWAProject/backend/rpc/python')
import backend_client
#mimetypes.add_type("image/svg+xml", ".svg", True)
#mimetypes.add_type("image/svg+xml", ".svgz", True)
# Create your views here.

# renders home page
def index(request):
    return render(request,'musician/index.html')

# login handler
def artist_login(request):
    if request.method == 'GET':
        if request.user.username != '':
            return redirect('/musician/artist/'+request.user.username)
        else:
            return render(request,'musician/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        login_user = authenticate(username=username, password=password)
        if login_user is not None:
            login(request, login_user)
            return redirect('/musician/artist/'+username+'/')
        else:
            messages.add_message(request, messages.ERROR, "Login Invalid, Please Try Again")
            return redirect('/musician/login')

# register handler
def register(request):
    if request.method == 'GET':
        return render(request,'musician/register.html')
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        login_user = authenticate(username=username, password=password)
        login(request, login_user)
        return redirect('/musician/artist/'+username+'/')

# logout user
def artist_logout(request):
    logout(request)
    return redirect('/musician')

# present a QR code on demand
@csrf_exempt
def getQRCode(request, music_id):
    # generate token - save to database
    # generate URL with token --> this will be a QR code to be displayed
    newMusic = Music.objects.get(id=music_id)
    stringToHash = str(time.time()) + str(newMusic.artist) + str(newMusic.title)
    h = hashlib.sha1()
    h.update(stringToHash)    
    tokenToAppendinURL = str(h.hexdigest())
    print 'created token: ' + tokenToAppendinURL

    # save music query to database 
    newQuery = MusicQuery(query=newMusic, token=tokenToAppendinURL)
    newQuery.save()

    #QR code to be displayed
    # url = pyqrcode.create('http://35.163.220.222:8000/musician/music/' + tokenToAppendinURL)
    # url = pyqrcode.create('http://54.209.248.145:8000/musician/music/' + tokenToAppendinURL)
    # url = pyqrcode.create('http://localhost:8000/musician/music/' + tokenToAppendinURL)
    url = pyqrcode.create(settings.ROOT_URL + '/musician/music/' + tokenToAppendinURL)

    # image_as_str = code.png_as_base64_str(scale=5)
    # html_img = '<img src="data:image/png;base64,{}">'.format(image_as_str)
    strToSave = 'musician/static/images/' + tokenToAppendinURL + '.png'
    url.png(strToSave, scale=6)  
    strToShow = '/static/images/' + tokenToAppendinURL + '.png'
    x = json.dumps({'qrpath': strToShow})
    return JsonResponse(x, safe=False)

# executed on QR code url
def music_query(request, token):
    context = {}
    if request.method == 'GET':
        # check token and serve page
        try:
            targetQuery = MusicQuery.objects.get(token=token)
            targetMusic = targetQuery.query
            context['music'] = targetMusic
            # context['url'] = 'http://35.163.220.222:8000/musician/download/' + token
            # context['url'] = 'http://54.209.248.145:8000/musician/download/' + token
            # context['url'] = 'http://localhost:8000/musician/download/' + token
            context['url'] = settings.ROOT_URL + '/musician/download/' + token
            context['showForm'] = True
        except Exception as e:
            context['showForm'] = False
        return render(request, 'musician/music.html',context)
    else:
        return redirect('/musician')

# download request handler
def download(request, token):
    context = {}
    if request.method == 'GET':
        try:
            # check token in database and retrieve corresponding music
            targetQuery = MusicQuery.objects.get(token=token)
            targetMusic = targetQuery.query
            file_name = targetMusic.file_name
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file_path = dir_path + '/music/' + file_name
            file_wrapper = FileWrapper(file(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)

            # store the download record
            newDownload = Download.objects.create(music=targetMusic, download_loc='')
            newDownload.save()

            # download the music file
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=' + file_name
            targetQuery.delete()
            return response
        except Exception as e:
            messages.add_message(request, messages.ERROR, "Music Download Failed: QR Code Expired")
            logging.exception("message")
            return redirect('/musician')
    else:
        return redirect('/musician')

# artist upload handler
def artist(request, artist_id):
    # The artist_id is identical with the auto-generated id created by User model
    if request.user.is_authenticated and request.user.username == artist_id:
        # Put whatever we want to display on artist page in context object
        # e.g. A list of music composed by this artist
        context = {}
        context['artist'] = artist_id
        if request.method == 'GET':  
            artistMusic = Music.objects.filter(artist=request.user)
            context["musics"] = artistMusic
            return render(request, 'musician/artist.html',context)
        else:
            try:
                # Create a new Music record
                newMusic = Music(artist=request.user, title=request.POST['title'], genre=request.POST['genre'], file_name="", rate=0, download_url="") 
                newMusic.save()
                # Retrieve the suffix of the file
                ext = find_ext(request.FILES['music'].name)
                # The Music ID is automatically created after save()
                newMusic.file_name = str(newMusic.id) + ext
                newMusic.save()
                dir_path = os.path.dirname(os.path.realpath(__file__))
                handle_uploaded_file(request.FILES['music'], dir_path+'/music/'+newMusic.file_name)
                messages.add_message(request, messages.INFO, "Music Upload Successful")
                return redirect('/musician/artist/'+artist_id)
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Music Upload Failed")
                logging.exception("message")
                return redirect('/musician/artist/'+artist_id)
    else:
        return redirect('/musician/login')

# statistics request handler
def statistics(request, artist_id, music_id):
    if request.user.is_authenticated and request.user.username == artist_id:
        context = {}
        context['artist'] = artist_id
        context['music_name'] = Music.objects.get(id=music_id).title
        today = datetime.now()
        stats = {}
        nodata = 1 
	for i in range(1,8):
	    target_day = today-timedelta(i)
            target_day = target_day.strftime("%Y-%m-%d")
            print target_day
            (date, count, rank) = backend_client.run_request(int(music_id),target_day)
	    if rank != 0:
                nodata = 0;
	        stats[i] = rank
        if nodata == 1:
            stats[0] = 0
        context['rank'] = stats;
        return render(request,'musician/statistics.html', context)
    else:
        messages.add_message(request, messages.ERROR, "No Access to This Page")
        logging.exception("message")
        return redirect('/musician/')
        
        
        
		
