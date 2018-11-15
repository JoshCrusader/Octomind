
from octo_site.models import *
from django.http import JsonResponse
from octo_site.db_conf import *

def get_market(request):
    market = []
    if(request.method == 'POST'):
        gid = request.POST['game_id']
        game = Game.objects.get(game_id = gid)
        market = game.get_market_data(game)
    return JsonResponse({"data": market})