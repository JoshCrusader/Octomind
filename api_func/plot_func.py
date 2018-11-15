from django.shortcuts import render
from octo_site.models import *
from octo_site.forms import *
from django.http import HttpResponseRedirect, JsonResponse
import pytz
from django.core import serializers
import json
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_plot(request):
    width = request.POST['width']
    height = request.POST['height']
    data = request.POST['coords']
    data = json.loads(data)
    print(data)
    print(height,width)
    for dat in data:
        print(dat['id'])
        tCoord = (float(dat['top_coordinate'].replace("px",""))/float(height))*100
        lCoord = (float(dat['left_coordinate'].replace("px",""))/float(width))*100
        sensor = Sensor.objects.get(sensor_id=dat['id'])
        sensor.top_coordinate = round(tCoord, 3)
        sensor.left_coordinate = round(lCoord, 3)
        sensor.save()
        print(sensor.top_coordinate,sensor.left_coordinate)
    return JsonResponse({'filename':"kapiha"})

@csrf_exempt
def get_log_distribution(request, game_ids):
    #must get all logs of each game to plot the sensor distribution between games
    data_return = {}
    gids = game_ids.split("-")
    games = []
    for g in gids:
        games.append(Game.objects.get(id=int(g)))
        data_return[str(g)] = None
    for game in games:
        data = game.pull_data_fr_game(game)

        for d in data:
            if int(d["value"]) == 1:
                data_return[str(game.game_id)].append(d)
    return JsonResponse({"data": data_return})

def get_log_summary(request,game_ids):
    '''
    :param request: 
    :param game_ids: slug of game ids
    :return: returns an average of all the sensor logs
    '''
    summary_ave_data = {}
    data_return = []
    gids = game_ids.split("-")
    games = []

    for g in gids:
        games.append(Game.objects.get(game_id=int(g)))
    for game in games:
        data = game.pull_data_game(game)
        for d in data:
            if int(d["time_solved"]) != 0:
                data_return.append(d)
    sensors = games[0].room.get_all_sensors
    for s in sensors:
        summary_ave_data[s.sensor_id] = {"sensor_id":s.sensor_id, "sensor_name":s.sensor_name, "avg_time_solved":0,"avg_min_stamped":0,"count":0}
    for d in data_return:
        for s in sensors:
            if d["sensor_id"] == s.sensor_id:
                summary_ave_data[s.sensor_id]["avg_time_solved"] += d["time_solved"]
                summary_ave_data[s.sensor_id]["avg_min_stamped"] += d["min_stamped"]
                summary_ave_data[s.sensor_id]["count"] += 1

    for sum_av in summary_ave_data:
        summary_ave_data[sum_av]["avg_time_solved"] = round(summary_ave_data[sum_av]["avg_time_solved"]/summary_ave_data[sum_av]["count"], 2)
        summary_ave_data[sum_av]["avg_min_stamped"] = round(summary_ave_data[sum_av]["avg_min_stamped"]/summary_ave_data[sum_av]["count"], 2)

    return JsonResponse({"data": summary_ave_data})
