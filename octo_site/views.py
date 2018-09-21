from django.shortcuts import render,redirect
from octo_site.models import *

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
    if user is not None and request.method == 'POST':
        request.session['username'] = user.username
        request.session['guest'] = True
        request.session['logged'] = True
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'octo_site/login.html')

'''
    TODO: Using sign up form, create a user
'''
def register(request):

    if(request.method == 'POST'):
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return render(request, 'octo_site/register.html')
    else:
        return render(request, 'octo_site/register.html')



def dashboard(request):
    return render(request,'octo_site/dashboard.html')
def signout(request):
    logout(request)
    return redirect('index')
def index(request):
    return render(request,'octo_site/dashboard.html')