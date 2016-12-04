from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os
from .models import Music, MusicQuery
import os, mimetypes
from wsgiref.util import FileWrapper
from .models import Music, Download
from handle_file import handle_uploaded_file, find_ext 
import hashlib
import pyqrcode
import time
import logging
import qrcode
#import mimetypes
import png

#mimetypes.add_type("image/svg+xml", ".svg", True)
#mimetypes.add_type("image/svg+xml", ".svgz", True)
# Create your views here.

def index(request):
    return render(request,'musician/index.html')

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

def artist_logout(request):
    logout(request)
    return redirect('/musician')


def download(request):
    return render(request,'musician/download.html')


def getQRCode(request, artist_id):
    print 'did it not get here'
    return redirect('musician/artist.html')

def download(request, file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = dir_path + '/music/' + file_name
    file_wrapper = FileWrapper(file(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    # Retrieve the Music Object and store the download record
    targetMusic = Music.objects.get(file_name=file_name);
    newDownload = Download.objects.create(music=targetMusic, download_loc='')
    newDownload.save()
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=' + file_name
    return response
    
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
                # The download url should be a music page
                newMusic = Music(artist=request.user, title=request.POST['title'], genre=request.POST['genre'], file_name="", rate=0, download_url="") 
                newMusic.save()
                # Retrieve the suffix of the file
                ext = find_ext(request.FILES['music'].name)
                # The Music ID is automatically created after save()
                newMusic.file_name = str(newMusic.id) + ext
                newMusic.save()

                # generate token - save to database
                # generate URL with token --> this will be a QR code to be displayed
                stringToHash = str(time.time()) + str(newMusic.artist) + str(newMusic.title)
                
                h = hashlib.sha1()
                h.update(stringToHash)
                
                tokenToAppendinURL = str(h.hexdigest())

                # save to database 
                newQuery = MusicQuery(query=newMusic, token=tokenToAppendinURL)
                newQuery.save()

                #QR code to be displayed
                url = pyqrcode.create('http://35.163.220.222:8000/musician/artist/'+ str(newMusic.artist) + '/' + str(newMusic.title) + '/' + 'token=' + tokenToAppendinURL)
                # image_as_str = code.png_as_base64_str(scale=5)
                # html_img = '<img src="data:image/png;base64,{}">'.format(image_as_str)
                strToSave = 'musician/static/images/' + tokenToAppendinURL + '.png'
                url.png(strToSave, scale=6)  
                url.show()

                #url.svg('uca-url.svg', scale=8)
                #print(url.terminal(quiet_zone=1))

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

def statistics(request, artist_id, music_id):
    if request.user.is_authenticated and request.user.username == artist_id:
        context['artist'] = artist_id
        return render(request,'musician/statistics.html')
