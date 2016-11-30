from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,'musician/index.html')

def login(request):
    return render(request,'musician/login.html')

def artist(request, artist_id):
    return HttpResponse("Hello %s" % artist_id)
