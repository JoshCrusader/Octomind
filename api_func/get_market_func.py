
from octo_site.models import *
from django.http import JsonResponse
from octo_site.db_conf import *


from utils import populate_rebeca, populate_details
def get_market(request):
    # populate_rebeca.main_start()
    market = []
    if(request.method == 'POST'):
        gid = request.POST['game_id']
        # game = Game.objects.get(game_id = gid)
        # market = game.get_market_data(game)
    return JsonResponse({"data": market})