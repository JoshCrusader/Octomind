
from octo_site.models import *
from django.http import JsonResponse
from octo_site.db_conf import *
import math
from datetime import datetime,timedelta
import datetime as dt

def get_players_cities(request):
    games = request.POST.getlist('games[]')
    cities = {}

    citynames = PlayersCity.objects.order_by('city').values('city').distinct()

    for cn in citynames:
        cities[cn['city']] = 0
    for gameid in games:
        game = Game.objects.get(game_id = gameid)
        players = game.get_players_fr_game(game)
        for player in players:
            if(player.loc_dictionary_id == 48):
                cityaddress = PlayersCity.objects.get(players_players_id = player)
                cities[cityaddress.city] += 1
    market = "sad"
    return JsonResponse({"data": cities})