from django.shortcuts import render
from octo_site.models import *
from octo_site.forms import *
from django.http import HttpResponseRedirect, JsonResponse
import pytz
from django.core import serializers
import json
from django.urls import reverse
from octo_site.exception_controller import *

def exception_report_details(request):
    room=""
    msg = ""
    has_result=False
    errors=""
    warnings=""
    games=None
    a_date = None
    a_sd = None
    a_ed = None
    if request.method == 'POST':
        room = Room.objects.get(room_id=request.POST['room_id'])
        if request.POST['report_cat'] == "range":
            a_sd = request.POST['sd']
            a_ed = request.POST['ed']
            print("to date range we go!")
            msg, games, errors, warnings = get_range_exception(request,room)
        elif request.POST['report_cat'] == "monthly":
            a_date = request.POST['date']
            msg, games, errors, warnings = get_monthly_exception(request,room)
        elif request.POST['report_cat'] == "yearly":
            a_date = request.POST['date']
            msg, games, errors, warnings = get_yearly_exception(request,room)
        elif request.POST['report_cat'] == "daily":
            a_date = request.POST['date']
            msg, games, errors, warnings = get_daily_exception(request,room)
        else:
            print("what")
    if len(games) !=0 or len(warnings) !=0 or len(errors) !=0:
        has_result=True
        print(len(games))
        print(len(warnings))
        print(len(errors))
    for e in errors:
        print(e.game.game_details.timestart)
    return render(request, 'octo_site/reports/details/exception_report_details.html',
                  {"has_result":has_result,
                   "msg":msg,
                   "games":games,
                   "errors": errors,
                   "warnings":warnings,
                   "room":room,
                   "room_id":request.POST['room_id'],
                   "rep_cat": request.POST['report_cat'],
                   "date" : a_date,
                   "sd": a_sd,
                   "ed": a_ed})
