
from octo_site.models import *
from django.http import JsonResponse
from octo_site.db_conf import *
import math
from datetime import datetime,timedelta
import datetime as dt

def get_range_games(request,room):
    games=[]
    sd = datetime.strptime(request.POST['sd'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['ed'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
            
    return games
def get_monthly_games(request,room):
    games = []
    month = datetime.strptime(request.POST['req_date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=month.year)

    for det in gamedet:
        if det.timestart.month == month.month:
            g = Game.objects.get(game_id=det.game_details_id)
            if g.room_id == room.room_id:
                games.append(g)
    return games
def get_yearly_games(request,room):
    games = []
    year = datetime.strptime(request.POST['req_date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=year.year)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
    return games
def get_daily_games(request,room):
    games = []
    sd = datetime.strptime(request.POST['req_date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['req_date'] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
    return games

def get_room_market(request):
    games = []
    market = {}
    market['f'] = 0
    market['m'] = 0
    market['length'] = 0
    market['locs'] = {}
    market['loc_titles'] = {}
    market['ages'] = {}
    market['teamsizes'] = {}
    if(request.method == 'POST'):
        req_cat = request.POST['req_cat']
        rid = request.POST['room_id']
        room = Room.objects.get(room_id = rid)
        if(req_cat == 'range'):
            games = get_range_games(request, room)
        elif(req_cat == 'monthly'):
            games = get_monthly_games(request, room)
        elif(req_cat == 'yearly'):
            games = get_yearly_games(request, room)
        elif(req_cat == 'daily'):
            games = get_daily_games(request, room)

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
        market['f'] += g_market['f']
        market['m'] += g_market['m']
        market['length'] += g_market['length']
        for key, value in g_market['locs'].items():
            try:
                market['locs'][key]['value'] += value
            except:
                market['locs'][key]['value'] = value
        for key, value in g_market['ages'].items():
            try:
                market['ages'][key] += value
            except:
                market['ages'][key] = value
        try:
            market['teamsizes'][g_market['length']] += 1
        except:
            market['teamsizes'][g_market['length']] = 1
    return JsonResponse({"data": market})