from django.shortcuts import render,redirect
from octo_site.models import *
from octo_site.forms import *
from django.http import HttpResponseRedirect, JsonResponse
import pytz
from django.core import serializers
import json
from django.urls import reverse

def game_logs(request):
    cur_games = []
    cur_inds = []
    gd = GameDetails.objects.filter(timeend__isnull=True)
    print("ekseluded")
    for g in gd:
        try:
            if g.game.is_ongoing:
                cur_games.append(Game.objects.get(game_id=g.game_details_id))
                cur_inds.append(g.game_details_id)
                print("ekseluded")
        except:
            pass
    all_g = Game.objects.filter(game_details__timestart__isnull=False)
    all_g.exclude(game_id__in=cur_inds)
    print("passing")
    return render(request, 'octo_site/game_logs/game_logs.html', {'games': all_g, 'cur_games': cur_games})

def game_logs_detail(request,game_id):
    g = Game.objects.get(game_id=game_id)
    summary = g.pull_game_summary(g)
    data_summary = g.pull_data_game(g)
    clues = g.get_data_clues
    senlogs = g.pull_data_fr_game(g)

    date_now = datetime.now().strftime("%Y-%m-%d")


    return render(request, 'octo_site/game_logs/game_logs_detail.html',
                  {'logs':senlogs,
                   'clues':clues,
                   'dt_now':date_now,
                   'clues_len':len(clues),
                   'game': g,
                   'errors': GameErrorLog.objects.filter(game_id=game_id),
                   'warnings': GameWarningLog.objects.filter(game_id=game_id),
                   'general_info':summary['general_info'],
                   'sensor_info': summary['sensor_info'],
                   'data_summary':data_summary})

def analyze_game_logs(request,game_ids):
    gids = game_ids.split("-")
    games = []
    date_now = datetime.now().strftime("%Y-%m-%d")
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

    #cohort analysis data
    total_players = 0
    first_time_players = {"player_count":None,"avg_completion_time":0,"avg_clues":0,"avg_anomalies":0}
    loyal_players = {"player_count":None, "avg_completion_time": 0, "avg_clues": 0, "avg_anomalies": 0}
    players_repeated = {"player_count":None, "avg_completion_time": 0, "avg_clues": 0, "avg_anomalies": 0}
    players_played_another = {"player_count":None, "avg_completion_time": 0, "avg_clues": 0, "avg_anomalies": 0}

    #get_some data
    for g in games:
        total_players += g.get_team_size_int

    return render(request, 'octo_site/game_logs/game_logs_analysis.html',
                  {"room_id":games[0].room_id,
                   "room": games[0].room,
                   "id_slugs": game_ids,
                   "game_count":len(games),
                   'dt_now':date_now,
                   'game_ids': gids,
                   "games": games})
