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
    sensor_ids={}
    sensor_dist={}
    s_w=[]
    s_f=[]
    s_e=[]
    orig = []
    rep = []
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    error_logs = GameErrorLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)
    warning_logs = GameWarningLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)

    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            if g.get_game_conclusion == 'forfeit':
                games.append(g)
                s = g.get_sensor_asked(g)
                if s not in orig:
                    orig.append(s)
                s_f.append(s)
                rep.append(s)

    for er in error_logs:
        g = Game.objects.get(game_id=er.game_id)
        if g.room_id == room.room_id:
            errors.append(er)
            if er.sensor_id not in orig:
                orig.append(er.sensor_id)

            s_e.append(er.sensor_id)
            rep.append(er.sensor_id)

    for wa in warning_logs:
        g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)
            if wa.sensor_id not in orig:
                orig.append(wa.sensor_id)
            s_w.append(wa.sensor_id)
            rep.append(wa.sensor_id)
    for o in orig:
        sensor_ids[o]=0

        for r in rep:
            if r == o:
                sensor_ids[o]+=1

        sensor_dist[o] = {
            "warnings": 0,
            "errors": 0,
            "forfeits": 0}
        for f in s_f:
            if f == o:
                sensor_dist[o]["forfeits"]+=1

        for e in s_e:
            if e == o:
                sensor_dist[o]["errors"]+=1

        for w in s_w:
            if w == o:
                sensor_dist[o]["warnings"]+=1

    print(sensor_dist)
    msg = "from " + str(sd.strftime("%B %d, %Y")) + " to " + str(ed.strftime("%B %d, %Y"))
    return msg,games,errors,warnings,sensor_ids,sensor_dist

def get_monthly_exception(request, room):
    games = []
    errors = []
    warnings = []
    sensor_ids={}
    sensor_dist={}
    s_w=[]
    s_f=[]
    s_e=[]
    orig = []
    rep = []
    dist = []

    month = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=month.year)
    error_logs = GameErrorLog.objects.filter(timestamp__year=month.year)
    warning_logs = GameWarningLog.objects.filter(timestamp__year=month.year)

    for det in gamedet:
        if det.timestart.month == month.month:
            g = Game.objects.get(game_id=det.game_details_id)
            if g.room_id == room.room_id:
                games.append(g)
                s = g.get_sensor_asked(g)
                if s not in orig:
                    orig.append(s)
                rep.append(s)
                s_f.append(s)

    for er in error_logs:
        if er.timestamp.month == month.month:
            g = Game.objects.get(game_id=er.game_id)
            if g.room_id == room.room_id:
                errors.append(er)
                if er.sensor_id not in orig:
                    orig.append(er.sensor_id)
                rep.append(er.sensor_id)
                s_e.append(er.sensor_id)

    for wa in warning_logs:
        if wa.timestamp.month == month.month:
            g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)
            if wa.sensor_id not in orig:
                orig.append(wa.sensor_id)
            rep.append(wa.sensor_id)
            s_w.append(wa.sensor_id)

    for o in orig:
        sensor_ids[o] = 0
        for r in rep:
            if r == o:
                sensor_ids[o] += 1

        sensor_dist[o] = {
            "warnings": 0,
            "errors": 0,
            "forfeits": 0}
        for f in s_f:
            if f == o:
                sensor_dist[o]["forfeits"]+=1
        for e in s_e:
            if e == o:
                sensor_dist[o]["errors"]+=1
        for w in s_w:
            if w == o:
                sensor_dist[o]["warnings"]+=1
    msg = "month of " + month.strftime("%b") + " " + str(month.year)
    return msg, games, errors, warnings,sensor_ids,sensor_dist

def get_yearly_exception(request, room):
    games = []
    errors = []
    warnings = []
    sensor_ids={}
    sensor_dist={}
    s_w=[]
    s_f=[]
    s_e=[]
    orig = []
    rep = []
    year = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=year.year)
    error_logs = GameErrorLog.objects.filter(timestamp__year=year.year)
    warning_logs = GameWarningLog.objects.filter(timestamp__year=year.year)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
            s = g.get_sensor_asked(g)
            if s not in orig:
                orig.append(s)
            rep.append(s)
            s_f.append(s)
    for er in error_logs:
        g = Game.objects.get(game_id=er.game_id)
        if g.room_id == room.room_id:
            errors.append(er)
            if er.sensor_id not in orig:
                orig.append(er.sensor_id)
            rep.append(er.sensor_id)
            s_e.append(er.sensor_id)
    for wa in warning_logs:
        g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)
            if wa.sensor_id not in orig:
                orig.append(wa.sensor_id)
            rep.append(wa.sensor_id)
            s_w.append(wa.sensor_id)
    for o in orig:
        sensor_ids[o] = 0
        for r in rep:
            if r == o:
                sensor_ids[o] += 1

        sensor_dist[o] = {
            "warnings": 0,
            "errors": 0,
            "forfeits": 0}
        for f in s_f:
            if f == o:
                sensor_dist[o]["forfeits"]+=1
        for e in s_e:
            if e == o:
                sensor_dist[o]["errors"]+=1
        for w in s_w:
            if w == o:
                sensor_dist[o]["warnings"]+=1

    msg = "year of" + str(year.year)
    return msg, games, errors, warnings,sensor_ids,sensor_dist


def get_daily_exception(request, room):
    games = []
    errors = []
    warnings = []
    sensor_ids={}
    sensor_dist={}
    s_w=[]
    s_f=[]
    s_e=[]
    orig = []
    rep = []
    sd = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['date'] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    error_logs = GameErrorLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)
    warning_logs = GameWarningLog.objects.filter(timestamp__gte=sd, timestamp__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
            s = g.get_sensor_asked(g)
            if s not in orig:
                orig.append(s)
            rep.append(s)
            s_f.append(s)
    for er in error_logs:
        g = Game.objects.get(game_id=er.game_id)
        if g.room_id == room.room_id:
            errors.append(er)
            if er.sensor_id not in orig:
                orig.append(er.sensor_id)
            rep.append(er.sensor_id)
            s_e.append(er.sensor_id)
    for wa in warning_logs:
        g = Game.objects.get(game_id=wa.game_id)
        if g.room_id == room.room_id:
            warnings.append(wa)
            if wa.sensor_id not in orig:
                orig.append(wa.sensor_id)
            rep.append(wa.sensor_id)
            s_w.append(wa.sensor_id)
    for o in orig:
        sensor_ids[o] = 0
        for r in rep:
            if r == o:
                sensor_ids[o] += 1
        sensor_dist[o] = {
            "warnings": 0,
            "errors": 0,
            "forfeits": 0}
        for f in s_f:
            if f == o:
                sensor_dist[o]["forfeits"] += 1
        for e in s_e:
            if e == o:
                sensor_dist[o]["errors"] += 1
        for w in s_w:
            if w == o:
                sensor_dist[o]["warnings"] += 1

    msg = "for " + str(sd.strftime("%B %d, %Y"))
    return msg, games, errors, warnings,sensor_ids,sensor_dist

