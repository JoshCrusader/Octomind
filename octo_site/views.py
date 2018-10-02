from django.shortcuts import render,redirect
from octo_site.models import *
from octo_site.forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import sys
from octo_site.db_conf import pull_data
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

def page_sensor(request):
    return render(request, 'octo_site/settings/sensor_page.html')
def page_venue(request):
    room_form = RoomForm()
    if request.method == 'POST':
        if request.POST['type'] == "room":
            room_form = RoomForm(request.POST, request.FILES)
            if room_form.is_valid():
                room = Room(room_name=request.POST['room_name'], branch_id=request.POST['branch_id'], header_img=request.FILES['header_img'])
                room.save()
        else:
            branch = Branch(name=request.POST['name'], address=request.POST['address'])
            branch.save()

    branches = Branch.objects.all()
    rooms = Room.objects.all()
    return render(request, 'octo_site/settings/venue_page.html',
                  {"branches":branches,"rooms":rooms,"room_form":room_form})

@csrf_exempt
def upload_process(request):
    print("waw ngaleng")
    return JsonResponse({'filename':"kapiha"})
def add_room(request):
    return render(request, 'octo_site/settings/venue_page.html')
def dashboard(request):
    return render(request,'octo_site/dashboard.html')
def signout(request):
    logout(request)
    return redirect('index')
def index(request):
    print("gago")
    return render(request,'octo_site/dashboard.html')
def control_panel(request):
    print("control panel")
    return render(request,'octo_site/control_panel.html', {'h': 5})
def sensor_data():
    return pull_data()

