from octo_site.models import *
from django.http import JsonResponse
from django.utils import timezone

def get_cur_games(request):
    if(request.method == 'POST'):
        rid = request.POST['room_id']
        gd = GameDetails.objects.filter(timestart__isnull = True)
        games = []
        for i in gd:
            game_objs = Game.objects.filter(game_details_id = i.game_details_id, room_id = rid)
            for i in game_objs:
                team_obj = {}
                gd_obj = GameDetails.objects.get(game_details_id = i.game_details_id)
                team_obj['teamname'] = gd_obj.teamname
                team_obj['gamedetail'] = gd_obj.game_details_id
                team_obj['game'] = i.game_id
                games.append(team_obj)
            
    return JsonResponse({"data": games})

def get_player_list(request):
    if(request.method == 'POST'):
        gid = request.POST['game_id']
        players = []
        team_query = Teams.objects.filter(game_id = gid)
        for team_item in team_query:
            player = Players.objects.get(players_id = team_item.players_players_id)
            player_obj = {}
            player_obj['name'] = player.firstname+' '+player.lastname
            players.append(player_obj)
    return JsonResponse({"data": players})

def start_game(request):
    if(request.method == 'POST'):
        gid = request.POST['game_id']
        now_datetime = timezone.now()
        game = Game.objects.get(game_id = gid)
        game_detail = GameDetails.objects.get(game_details_id = game.game_details_id)
        game_detail.timestart = now_datetime
        game_detail.save()

    return JsonResponse({"data": "done"})

def end_game(request):
    if(request.method == 'POST'):
        gid = request.POST['game_id']
        now_datetime = timezone.now()
        game_detail = GameDetails.objects.get(game_details_id = gid)
        game_detail.timeend = now_datetime
        game_detail.save()
    return JsonResponse({"data": "done"})

def add_clue(request):
    if(request.method == 'POST'):
        cval = request.POST['clue_desc']
        gid = request.POST['gameid']
        now_datetime = timezone.now()
        cdetail = ClueDetails(detail = cval, timestamp = now_datetime)
        cdetail.save()
        clue = Clues(clue_details_id = cdetail.clue_details_id, game_id = gid)
        clue.save()
    return JsonResponse({"data": "done"})

def get_clues_by_game(game_id):
    data_return=[]
    clues = Clues.objects.filter(game_id=game_id)
    for c in clues:
        data_return.append({
            "clue_id": c.clue_id,
            "sensor_asked": c.clue_details.get_sensor_asked,
            "minute_asked": c.clue_details.get_minute_asked,
            "detail": c.clue_details.detail,
            "timestamp": c.clue_details.timestamp})
    return JsonResponse({"data": data_return})
