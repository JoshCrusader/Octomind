from django.utils import timezone
from django.shortcuts import render
from octo_site.models import *
import json

def tv_monitor(request, game_id):

    properties = {}
    try:
        game = Game.objects.get(game_id = game_id)
        if(game is not None):
            details = GameDetails.objects.get(game_details_id = game.game_details_id)
            now_datetime = timezone.now()
            properties['gameid'] = game_id
            properties['timeend'] = details.timestart + timezone.timedelta(hours=1)+ timezone.timedelta(minutes=1)
            if(details.timestart + timezone.timedelta(hours=1) > now_datetime):
                properties['done'] = False
                properties['minutes'] = (details.timestart + timezone.timedelta(hours=1) - now_datetime).seconds // 60
                properties['seconds'] = (details.timestart + timezone.timedelta(hours=1) - now_datetime).seconds % 60
            else:
                properties['done'] = True

            if(details.timeend is not None):
                properties['done'] = True
    except Exception as e:
        print("no monitor")
    return render(request,'octo_site/view_room_assets/tv_monitor.html', properties)