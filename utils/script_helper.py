from octo_site.models import *
from django.http import JsonResponse
from django.utils import timezone



def add_mins(request):
    if(request.method == 'POST'):

        gid = request.POST['gid']
        game = Game.objects.get(game_id = gid)
        gd = game.game_details
        gd.timestart -= timezone.timedelta(minutes = 5)
        gd.save()

    return JsonResponse({"data": "YES"})
