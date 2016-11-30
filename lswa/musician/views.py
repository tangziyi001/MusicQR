from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.

def index(request):
    return render(request,'musician/index.html')

def login(request):
    return render(request,'musician/login.html')

def register(request):
    if request.method == 'GET':
        return render(request,'musician/register.html')
    else:
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.object.create_user(name, email, password)
        user.save()
        return render(request,'musician/login.html')

def download(request):
    return render(request,'musician/download.html')

def artist(request, artist_id):
    return HttpResponse("Hello %s" % artist_id)

def statistics(request, artist_id):
    return render(request,'musician/statistics.html')
