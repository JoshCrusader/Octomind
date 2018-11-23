from utils import federate
from django.utils import timezone
from django.shortcuts import render,redirect
from octo_site.models import *
import datetime
import json
def control_panel(request):
    if request.method == 'GET':
        federate.sync()
        game_details = []
        now_datetime = timezone.now()
        finish_time = now_datetime - timezone.timedelta(hours = 1)

        for i in GameDetails.objects.all().filter(timestart__gte = finish_time).filter(timeend__isnull = True):
            game_details.append(i)
        games = {}
        for g_d in game_details:
            i = Game.objects.get(game_details_id = g_d.game_details_id)
            games[i.room_id] = {}
            games[i.room_id]['game_id'] = i.game_id
            games[i.room_id]['game'] = (Room.objects.get(room_id = i.room_id))
            ## GETTING TIME DETAILS
            game_detail = GameDetails.objects.get(game_details_id = i.game_details_id)
            games[i.room_id]['minutes'] = (game_detail.timestart + timezone.timedelta(hours = 1) - now_datetime).seconds//60
            games[i.room_id]['seconds'] = (game_detail.timestart + timezone.timedelta(hours = 1) - now_datetime).seconds%60
            ## GETTING PLAYERS DETAILS
            teams = Teams.objects.filter(game_id = i.game_id)
            games[i.room_id]['players'] = []
            for team in teams:
                games[i.room_id]['players'].append(Players.objects.get(players_id = team.players_players_id))
            ## CLUES
            clues = Clues.objects.filter(game_id = i.game_id)
            games[i.room_id]['clues'] = range(0, 3-len(clues))
            games[i.room_id]['mystery'] = range(0, len(clues))
            print(len(clues))
        #for i in games[3]['players']:
        #    print(i.firstname)
        properties = {}
        properties['h'] = 5
        properties['rooms'] = Room.objects.all()
        properties['games'] = games
        return render(request,'octo_site/control_panel.html', properties)