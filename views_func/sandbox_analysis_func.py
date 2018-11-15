from django.shortcuts import render
from octo_site.models import *
import json

def sandbox_analysis(request, room_id):
    if(request.method == 'GET'):
        room_obj = Room.objects.get(room_id = room_id)
        properties = {}
        properties['roomid'] = room_obj.room_id
        properties['img'] = room_obj.header_img
        properties['roomname'] = room_obj.room_name
        properties['blueprint'] = room_obj.blueprint_file
    return render(request,'octo_site/reports/sandbox_analysis.html', properties)