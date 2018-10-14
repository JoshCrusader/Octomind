from django.shortcuts import render,redirect
from octo_site.models import *
import json
from django.http import HttpResponseRedirect, JsonResponse
from octo_site.forms import *
from django.core import serializers
import socket
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import sys
from octo_site.db_conf import pull_data,pull_data_room
from django.contrib.auth.decorators import login_required

import gspread
##gc = gspread.authorize(credentials)

from django.http import HttpResponse
# Create your views here
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
    if request.method == 'POST':
        print("posted, bitches",request.POST['type'])
        if request.POST['type'] == "sensor":
            add_sensor(request)
        elif request.POST['type'] == "sensor_type":
            add_sensor_type(request)
        elif request.POST['type'] == "rpi":
            add_rpi(request)
        elif request.POST['type'] == "edit_sensor":
            edit_sensor(request)
        elif request.POST['type'] == "edit_sensor_type":
            edit_sensor_type(request)
        elif request.POST['type'] == "edit_rpi":
            edit_rpi(request)
        elif request.POST['type'] == "delete_sensor":
            delete_sensor(request)
        return HttpResponseRedirect(reverse('page_sensor'))
    return render(request, 'octo_site/settings/sensor_page.html',{"sensors":Sensor.objects.all(),"rooms":Room.objects.all(),"sensor_type":SensorType.objects.all(),"rpi":Rpi.objects.all()})
def page_venue(request):

    if request.method == 'POST':
        if request.POST['type'] == "room":
            add_room(request)
        elif request.POST['type'] == "room_edit":
            edit_room(request)
        elif request.POST['type'] == "room_delete":
            delete_room(request)
        elif request.POST['type'] == "branch":
            add_branch(request)
        elif request.POST['type'] == "branch_edit":
            edit_branch(request)
        elif request.POST['type'] == "branch_delete":
            delete_branch(request)
        return HttpResponseRedirect(reverse('page_venue'))
    return render(request, 'octo_site/settings/venue_page.html',
                  {"branches":Branch.objects.all(),"rooms":Room.objects.all(),"room_form":RoomForm(),"edit_room_form":EditRoomForm()})

def control_panel(request):
    if request.method == 'GET':
        games = {}
        for i in Game.objects.all():
            games[i.room_id] = (Room.objects.get(room_id = i.room_id))
        print(games)
        properties = {}
        properties['h'] = 5
        properties['rooms'] = Room.objects.all()
        properties['games'] = games
        return render(request,'octo_site/control_panel.html', properties)
        pass

def access_room(request):
    ## Add Room in the game room
    if request.method == 'POST':
        pass


@csrf_exempt
def upload_process(request):
    return JsonResponse({'filename':"kapiha"})

@csrf_exempt
def get_sensors_by_room_id(request,room_id):
    data_return = []
    for sensor in Room.objects.get(room_id=room_id).get_all_sensors:
        data_return.append({"sensor_id":sensor.sensor_id,"sensor_name": sensor.sensor_name, "rpi_id": sensor.rpi_id, "sensor_type_id": sensor.sensor_type_id, "sequence_number": sensor.sequence_number})
    return JsonResponse({"sensors":data_return})
def dashboard(request):
    return render(request,'octo_site/dashboard.html')
def signout(request):
    logout(request)
    return redirect('index')
def index(request):
    print("gago")
    return render(request,'octo_site/dashboard.html')
@csrf_exempt
def sensor_data(request,room_id):
    print("room_id: ",room_id)
    data = pull_data_room(room_id)
    for d in data:
        sensor = Sensor.objects.get(sensor_id=d['sensor_id'])
        d['sensor_name'] = sensor.sensor_name
        d['rpi_id'] = sensor.rpi_id
        d['sensor_type_id'] = sensor.sensor_type_id
    return JsonResponse({"data": data})
def data_vis(request, room_id):
    room = Room.objects.get(room_id=room_id)
    return render(request,'octo_site/data_vis.html',{"room":room})
def add_room(request):
    if RoomForm(request.POST, request.FILES).is_valid():
        room = Room(room_name=request.POST['room_name'], branch_id=request.POST['branch_id'],
                    header_img=request.FILES['header_img'])
        room.save()
def add_branch(request):
    branch = Branch(name=request.POST['name'], address=request.POST['address'])
    branch.save()
def add_sensor(request):
    sensor = Sensor(sensor_name=request.POST['sensor_name'], rpi_id=request.POST['sensor_rpi_id'],
                sensor_type_id=request.POST['sensor_sensor_type_id'])
    sensor.sequence_number = sensor.get_sequence_number
    sensor.save()
def add_sensor_type(request):
    sensor_type = SensorType(sensor_type_name=request.POST['sensor_type_name'], val_name=request.POST['val_name'],
                trigger_treshold=request.POST['trigger_treshold'])
    sensor_type.save()
def add_rpi(request):
    try:
        socket.inet_aton(request.POST['ip_address'])
        rpi = Rpi(name=request.POST['name'], ip_address=request.POST['ip_address'],
                  room_id=request.POST['room_id'])
        rpi.save()
    except socket.error:
        messages.warning(request, 'IP Address is invalid, please enter another IP.')
def edit_sensor(request):
    sensor = Sensor.objects.get(sensor_id=request.POST['sensor_id'])
    sensor.sensor_name = request.POST['sensor_name']
    sensor.sensor_type_id = request.POST['sensor_sensor_type_id']
    sensor.rpi_id = request.POST['sensor_rpi_id']

    sensor.save()
def edit_room(request):
    room = Room.objects.get(room_id=request.POST['room_id'])
    room.room_name = request.POST['room_name']
    room.branch_id = request.POST['branch_id']
    try:
        sequences = request.POST['game_sequence'].split(",")
        for i,s in enumerate(sequences,1):
            change_sequence =  Sensor.objects.get(sensor_id=int(s))
            print("sensor_id: ", s, "| ctr: ",i)
            change_sequence.sequence_number = i
            change_sequence.save()
    except:
        pass
    room.save()
def edit_branch(request):
    branch = Branch.objects.filter(branch_id=request.POST['branch_id'])[0]
    branch.name = request.POST['name']
    branch.address = request.POST['address']
    branch.save()
def edit_sensor_type(request):
    sensor_type = SensorType.objects.get(sensor_type_id=request.POST['sensor_type_id'])
    sensor_type.sensor_type_name = request.POST['sensor_type_name']
    sensor_type.val_name = request.POST['val_name']
    sensor_type.trigger_treshold = request.POST['trigger_treshold']
    sensor_type.save()
def edit_rpi(request):
    rpi = Rpi.objects.get(rpi_id=request.POST['rpi_id'])
    rpi.name = request.POST['name']
    rpi.ip_address = request.POST['ip_address']
    rpi.room_id = request.POST['room_id']
    rpi.save()
def delete_sensor(request):
    sensor = Sensor.objects.get(sensor_id=request.POST['sensor_id'])
    sensor.delete()
def delete_room(request):
    room = Room.objects.filter(room_id=request.POST['room_id'])
    room.delete()
def delete_branch(request):
    branch = Branch.objects.filter(branch_id=request.POST['branch_id'])
    branch.delete()

def room_analysis(request):

    return render(request, 'octo_site/reports/room_analysis.html',{"rooms":Room.objects.all()})
def sensor_analysis(request):
    return render(request, 'octo_site/reports/sensor_analysis.html')
def trend_analysis(request):
    return render(request, 'octo_site/reports/trend_analysis.html')
