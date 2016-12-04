from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os, mimetypes
from wsgiref.util import FileWrapper
from .models import Music, Download
from handle_file import handle_uploaded_file, find_ext 
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
                dir_path = os.path.dirname(os.path.realpath(__file__))
                handle_uploaded_file(request.FILES['music'], dir_path+'/music/'+newMusic.file_name)
                messages.add_message(request, messages.INFO, "Music Upload Successful")
                return redirect('/musician/artist/'+artist_id)
            except Exception:
                messages.add_message(request, messages.ERROR, "Music Upload Failed")
                return redirect('/musician/artist/'+artist_id)
    else:
        return redirect('/musician/login')

def statistics(request, artist_id, music_id):
    if request.user.is_authenticated and request.user.username == artist_id:
        context['artist'] = artist_id
        return render(request,'musician/statistics.html')
