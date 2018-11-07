import MySQLdb
from octo_site.models import *
from octo_site.db_conf import *
import math
from datetime import datetime,timedelta
import datetime as dt
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
host = "localhost"
def compute_report_data(games):
    report_data = {"win":0,
                   "loss":0,
                   "completion_rate":0,
                   "avg_clues_asked":0,
                   "avg_duration":0,
                   "has_errors":0,
                   "warnings":0
                   }
    for g in games:
        if g.is_solved:
            report_data["win"] += 1
        else:
            report_data["loss"] += 1
        if g.has_error:
            report_data["has_errors"] += 1
        if g.has_warning:
            report_data["warnings"] += 1

        report_data["avg_clues_asked"] += g.get_num_clues_asked
        report_data["avg_duration"] += g.get_duration


    report_data["completion_rate"] = round((report_data["win"]/float(len(games)))*100, 2)
    report_data["avg_clues_asked"] = round((report_data["avg_clues_asked"]/float(len(games))), 2)
    report_data["avg_duration"] = round((report_data["avg_duration"] / float(len(games))), 2)

    report_data["has_errors"] = round((report_data["has_errors"]/float(len(games)))*100, 2)
    report_data["warnings"] = round((report_data["warnings"]/float(len(games)))*100, 2)

    return report_data
def get_range_report(request,room):
    games=[]
    sd = datetime.strptime(request.POST['sd'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['ed'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    for det in gamedet:
        games.append(Game.objects.get(game_id=det.game_details_id))
    print("games len", len(games))
    for g in games:
        if g.room_id != room.room_id:
            games.remove(g)
    msg = "from " + str(sd.strftime("%B %d, %Y")) + " to " + str(ed.strftime("%B %d, %Y"))
    return compute_report_data(games),msg,games
def get_monthly_report(request,room):
    games = []
    month = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    print("MONTH", month.date())
    print("MONTH",month.month)
    gamedet = GameDetails.objects.filter(timestart__year=month.year)

    print("det len", gamedet)
    for det in gamedet:
        if det.timestart.month == month.month:
            games.append(Game.objects.get(game_id=det.game_details_id))
        else:
            print("removed!" , det.timestart.month)
    for g in games:
        if g.room_id != room.room_id:
            games.remove(g)
    print("games len", len(games))
    msg = "month of " + month.strftime("%b") + " " + str(month.year)
    return compute_report_data(games), msg, games
def get_yearly_report(request,room):
    games = []
    year = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=year.year)
    for det in gamedet:
        games.append(Game.objects.get(game_id=det.game_details_id))

    for g in games:
        if g.room_id != room.room_id:
            games.remove(g)

    print("games len", len(games))
    msg = "year of" + str(year.year)
    return compute_report_data(games), msg, games
def get_daily_report(request,room):
    games = []
    date = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    sd = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['date'] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    print("det len", gamedet)
    for det in gamedet:
        games.append(Game.objects.get(game_id=det.game_details_id))
    print("games len",len(games))
    for g in games:
        if g.room_id != room.room_id:
            games.remove(g)
    msg = "for " + str(date.strftime("%B %d, %Y"))
    return compute_report_data(games), msg, games