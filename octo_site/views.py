from django.shortcuts import render,redirect
from octo_site.models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here
def log_in(request):

    print("loging doging")
    user = None
    try:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
    except:
        None
    if request.method == 'POST':
        if user is not None:
            request.session['username'] = user.username
            request.session['guest'] = True
            request.session['logged'] = True
            login(request, user)
        else:
            messages.warning(request,'Wrong credentials, please try again.')
        return redirect('index')
    else:
        return render(request, 'octo_site/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        print(user.username)
        messages.warning(request, 'Account Created.')
        return redirect('index')
    return render(request, 'octo_site/register.html')

def add_sensor(request):
    return render(request,'octo_site/settings/addsensor.html')
def add_room(request):
    return render(request,'octo_site/settings/addroom.html')
def add_branch(request):
    return render(request,'octo_site/settings/addbranch.html')

def dashboard(request):
    return render(request,'octo_site/dashboard.html')
def signout(request):
    logout(request)
    return redirect('index')
def index(request):

    print("gago")
    return render(request,'octo_site/dashboard.html')