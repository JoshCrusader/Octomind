from django.shortcuts import render,redirect
from octo_site.models import *
from octo_site.forms import *
from django.http import HttpResponseRedirect, JsonResponse
import pytz
from django.core import serializers
import json
from django.urls import reverse

def game_logs(request):
    utc = pytz.UTC
    cur_games = []
    cur_inds = []
    all_g = Game.objects.all()
    all_g2 =[]
    gd = GameDetails.objects.filter(timeend__isnull=True)
    for g in gd:
        diff = datetime.now().replace(tzinfo=utc) - g.timestart.replace(tzinfo=utc)
        days = diff.days
        days_to_hours = days * 24
        diff_btw_two_times = diff.seconds / 3600
        overall_hours = days_to_hours + diff_btw_two_times
        #difference between time and now is less than 1 hour, then it is a past game.
        if overall_hours < 1:
            cur_games.append(Game.objects.get(game_id=g.game_details_id))
            cur_inds.append(g.game_details_id)
    for ag in all_g:
        if ag.game_id not in cur_inds:
            all_g2.append(ag)
    return render(request, 'octo_site/game_logs/game_logs.html', {'games': all_g2, 'cur_games': cur_games})

def game_logs_detail(request,game_id):
    g = Game.objects.get(game_id=game_id)
    summary = g.pull_game_summary(g)
    data_summary = g.pull_data_game(g)
    senlogs = g.pull_data_fr_game(g)
    for d in senlogs:
        sensor = Sensor.objects.get(sensor_id=d['sensor_id'])
        d['sensor_name'] = sensor.sensor_name
        d['rpi_id'] = sensor.rpi_id
        d['sensor_type_id'] = sensor.sensor_type_id
    return render(request, 'octo_site/game_logs/game_logs_detail.html',
                  {'logs':senlogs,'game': g,'general_info':summary['general_info'],'sensor_info': summary['sensor_info'],'data_summary':data_summary})

def analyze_game_logs(request,game_ids):
    gids = game_ids.split("-")
    games = []
    try:
        gids = [int(i) for i in gids]
        room_id = Game.objects.get(game_id=game_ids.split("-")[0]).room_id
        for g in gids:
            if Game.objects.get(game_id=g).room_id != room_id:
                return redirect('error404')

    except:
        return redirect('error404')

    xd = set([x for x in gids if gids.count(x) > 1])
    if xd != set():
        return redirect('error404')
    for g in gids:
        games.append(Game.objects.get(game_id=g))
    return render(request, 'octo_site/game_logs/game_logs_analysis.html',
                  {"room_id":games[0].room_id,"room": games[0].room, "id_slugs": game_ids, "game_count":len(games),'game_ids': gids, "games": games})
