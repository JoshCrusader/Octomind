from django.shortcuts import render
from octo_site.models import *
from octo_site.forms import *
from django.http import HttpResponseRedirect, JsonResponse
import pytz
from django.core import serializers
import json
from django.urls import reverse

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
    return render(request, 'octo_site/settings/sensor_page.html',{"sensors":Sensor.objects.all().reverse(),"rooms":Room.objects.all(),"sensor_type":SensorType.objects.all(),"rpi":Rpi.objects.all()})
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

def add_room(request):
    if RoomForm(request.POST, request.FILES).is_valid():
        room = Room(room_name=request.POST['room_name'], branch_id=request.POST['branch_id'],
                    header_img=request.FILES['header_img'], blueprint_file=request.FILES['blueprint_file'])
        room.save()
def add_branch(request):
    branch = Branch(name=request.POST['name'], address=request.POST['address'])
    branch.save()
def add_sensor(request):
    sensor = Sensor(sensor_name=request.POST['sensor_name'], rpi_id=request.POST['sensor_rpi_id'],
                sensor_type_id=request.POST['sensor_sensor_type_id'],phase_name=request.POST['phase_name'])
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