
from octo_site.models import *
from django.http import JsonResponse
from octo_site.db_conf import *
import math
from datetime import datetime,timedelta
import datetime as dt

def get_monthly_games(request):
    games = []
    # month = datetime.strptime(request.POST['req_date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    month = timezone.now()

    gamedet = GameDetails.objects.filter(timestart__year=month.year).filter(timestart__month=month.month)

    for det in gamedet:
        if det.timestart.month == month.month:
            g = Game.objects.get(game_id=det.game_details_id)
            games.append(g)
    return games
def get_all_market(request):
    games = []
    market = {}
    market['locs'] = {}
    market['loc_titles'] = {}
    if(request.method == 'POST'):
        games = get_monthly_games(request)
       # gid = request.POST['game_id']
       # game = Game.objects.get(game_id = gid)
       # market = game.get_market_data(game)

    all_locs = LocDictionary.objects.all()
    for i in all_locs:
        market['locs'][i.loc_code] = {}
        market['locs'][i.loc_code]['value'] = 0
        market['locs'][i.loc_code]['title'] = i.loc_title

    for game in games:
        g_market = game.get_market_data(game)
        for key, value in g_market['locs'].items():
            try:
                market['locs'][key]['value'] += value
            except:
                market['locs'][key]['value'] = value
    return JsonResponse({"data": market})