from octo_site.models import *
from django.http import JsonResponse
from octo_site.db_conf import *
import math
from datetime import datetime, timedelta
import datetime as dt

#need fields: date,sd,ed,req_cat,room_id
def get_range_exception(request, room):
    sd = datetime.strptime(request.POST['sd'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['ed'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')

    games = [] #forfeited games
    errors = [] #game error log
    warnings = [] #game warning log
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    error_logs = GameErrorLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)
    warning_logs = GameWarningLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)

    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            if g.get_game_conclusion == 'forfeit':
                games.append(g)

    for er in error_logs:
        g = Game.objects.get(game_id=er.game_id)
        if g.room_id == room.room_id:
            errors.append(er)

    for wa in warning_logs:
        g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)

    msg = "from " + str(sd.strftime("%B %d, %Y")) + " to " + str(ed.strftime("%B %d, %Y"))
    return msg,games,errors,warnings

def get_monthly_exception(request, room):
    games = []
    errors = []
    warnings = []
    month = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=month.year)
    error_logs = GameErrorLog.objects.filter(timestamp__year=month.year)
    warning_logs = GameWarningLog.objects.filter(timestamp__year=month.year)

    for det in gamedet:
        if det.timestart.month == month.month:
            g = Game.objects.get(game_id=det.game_details_id)
            if g.room_id == room.room_id:
                games.append(g)
    for er in error_logs:
        if er.timestamp.month == month.month:
            g = Game.objects.get(game_id=er.game_id)
            if g.room_id == room.room_id:
                errors.append(er)

    for wa in warning_logs:
        if wa.timestamp.month == month.month:
            g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)
    msg = "month of " + month.strftime("%b") + " " + str(month.year)
    return msg, games, errors, warnings


def get_yearly_exception(request, room):
    games = []
    errors = []
    warnings = []
    year = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=year.year)
    error_logs = GameErrorLog.objects.filter(timestamp__year=year.year)
    warning_logs = GameWarningLog.objects.filter(timestamp__year=year.year)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
    for er in error_logs:
        g = Game.objects.get(game_id=er.game_id)
        if g.room_id == room.room_id:
            errors.append(er)
    for wa in warning_logs:
        g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)

    msg = "year of" + str(year.year)
    return msg, games, errors, warnings


def get_daily_exception(request, room):
    games = []
    errors = []
    warnings = []
    sd = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['date'] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    error_logs = GameErrorLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)
    warning_logs = GameWarningLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
    for er in error_logs:
        g = Game.objects.get(game_id=er.game_id)
        if g.room_id == room.room_id:
            errors.append(er)
    for wa in warning_logs:
        g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)

    msg = "for " + str(sd.strftime("%B %d, %Y"))
    return msg, games, errors, warnings

