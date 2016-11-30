from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'musician/index.html')

def artist_login(request):
    if request.method == 'GET':
        return render(request,'musician/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        login_user = authenticate(username=username, password=password)
        if login_user is not None:
            login(request, login_user)
            return redirect('/musician/artist/'+username+'/')
        else:
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

def download(request):
    return render(request,'musician/download.html')

@login_required
def artist(request, artist_id):
    if request.user.is_authenticated and request.user.username == artist_id:
        return HttpResponse("Hello %s" % artist_id)
    else:
        return redirect('login')

@login_required
def statistics(request, artist_id):
    return render(request,'musician/statistics.html')
