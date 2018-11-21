import MySQLdb
from octo_site.models import *
from octo_site.db_conf import *
import math
from datetime import datetime,timedelta
import datetime as dt
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
host = "localhost"
def compute_report_data(warning,error):
    report_data = {"errors":0,
                   "warnings":0,
                   "has_result": True
                   }
    try:
        pass
    except:
        report_data["completion_rate"] = None
        report_data["avg_clues_asked"] = None
        report_data["avg_duration"] = None
        report_data["has_errors"] = None
        report_data["warnings"] = None
        report_data["has_result"] = False
        print("no results found")
    return report_data
def get_range_report(request,room):
    games=[]
    game_ids=[]
    sd = datetime.strptime(request.POST['sd'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['ed'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
            game_ids.append(g.game_id)
    print("games len", len(games))
    msg = "from " + str(sd.strftime("%B %d, %Y")) + " to " + str(ed.strftime("%B %d, %Y"))
    return compute_report_data(games),msg,games,"-".join(map(str,game_ids))
def get_monthly_report(request,room):
    games = []
    game_ids=[]
    month = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=month.year)

    for det in gamedet:
        if det.timestart.month == month.month:
            g = Game.objects.get(game_id=det.game_details_id)
            if g.room_id == room.room_id:
                games.append(g)
                game_ids.append(g.game_id)
        else:
            print("removed!" , det.timestart.month)
    msg = "month of " + month.strftime("%b") + " " + str(month.year)
    return compute_report_data(games), msg, games,"-".join(map(str,game_ids))
def get_yearly_report(request,room):
    games = []
    game_ids=[]
    year = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=year.year)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
            game_ids.append(g.game_id)
    print("games len", len(games))
    msg = "year of" + str(year.year)
    return compute_report_data(games), msg, games,"-".join(map(str,game_ids))
def get_daily_report(request,room):
    games = []
    game_ids=[]
    date = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    sd = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['date'] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    print("det len", gamedet)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        if g.room_id == room.room_id:
            games.append(g)
            game_ids.append(g.game_id)
    msg = "for " + str(date.strftime("%B %d, %Y"))
    return compute_report_data(games), msg, games,"-".join(map(str,game_ids))