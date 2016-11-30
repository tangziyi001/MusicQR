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
    return render(request,'musician/register.html')

def download(request):
    return render(request,'musician/download.html')

def artist(request, artist_id):
    return HttpResponse("Hello %s" % artist_id)

def statistics(request, artist_id):
    return render(request,'musician/statistics.html')
