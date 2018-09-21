from django.shortcuts import render,redirect
from octo_site.models import *
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def log_in(request):
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
def signout(request):
    logout(request)
    return redirect('index')
def register(request):
    return render(request, 'octo_site/register.html')
def index(request):
    return render(request,'octo_site/dashboard.html')