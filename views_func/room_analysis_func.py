from django.shortcuts import render
from octo_site.models import *
from octo_site.forms import *
from django.http import HttpResponseRedirect, JsonResponse
import pytz
from django.core import serializers
import json
from django.urls import reverse
from octo_site.reports_controller import *

def room_details_analysis(request):
    report_data=""
    room=""
    msg = ""
    gamedet=""
    games=None
    game_ids=None
    if request.method == 'POST':
        room = Room.objects.get(room_id=request.POST['room_id'])
        if request.POST['report_cat'] == "range":
            report_data,msg,games,game_ids = get_range_report(request,room)
        elif request.POST['report_cat'] == "monthly":
            report_data, msg, games ,game_ids= get_monthly_report(request,room)
        elif request.POST['report_cat'] == "yearly":
            report_data, msg, games ,game_ids= get_yearly_report(request,room)
        elif request.POST['report_cat'] == "daily":
            report_data, msg, games,game_ids = get_daily_report(request,room)
        else:
            print("what")

    return render(request, 'octo_site/reports/details/room_details_analysis.html',{"report_data":report_data,"msg":msg,"games":games,"room":room,"room_id":request.POST['room_id'],"id_slugs": game_ids,"records_len":len(games)})
