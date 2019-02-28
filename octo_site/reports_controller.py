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
                   "warnings":0,
                   "sensor_most_clue_asked":'',
                   "sensor_asked_breakdown":'',
                   "clueitem_most_asked": '',
                   "clueitem_breakdown":'',
                   "has_result": True
                   }
    clues = {}
    sensors = {}
    report_clue=[]
    report_sensors=[]
    for sensor in Room.objects.get(room_id=games[0].room_id).get_all_sensors:
        sensors[sensor.sensor_id] = 0
    for ci in ClueItem.objects.filter(room_id=games[0].room_id):
        clues[ci.id] = 0

    for g in games:
        for clue in Clues.objects.filter(game_id=g.game_id):
            clues[ClueItemDetails.objects.get(clue_id=clue.clue_id).clue_item_id] += 1
            sensors[clue.clue_details.get_sensor_asked] += 1
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

    try:
        for key,value in clues.items():
            if value >0:
                report_clue.append({"id":key,"details":ClueItem.objects.get(id=key).detail,"count":value})
        for key,value in sensors.items():
                sensor = Sensor.objects.get(sensor_id=key)
                report_sensors.append({"id": sensor.sensor_id,
                                         "sensor_name": sensor.sensor_name,
                                        "phase_name": sensor.phase_name,
                                        "count": value})

        max_value = max(clues.values())  # maximum value
        max_keys = [k for k, v in clues.items() if v == max_value]
        clue_item = ClueItem.objects.get(id=max_keys[0])
        report_data['clueitem_most_asked'] = {"id":clue_item.id,
                                              "details":clue_item.detail,
                                              "count":max_value}
        max_value = max(sensors.values())  # maximum value
        max_keys = [k for k, v in sensors.items() if v == max_value]
        sensor = Sensor.objects.get(sensor_id=max_keys[0])
        report_data['sensor_most_clue_asked'] = {"id": sensor.sensor_id,
                                                 "sensor_name": sensor.sensor_name,
                                              "phase_name": sensor.phase_name,
                                              "count": max_value}
        report_data['clueitem_breakdown'] = report_clue
        report_data['sensor_asked_breakdown'] = report_sensors

        report_data["completion_rate"] = round((report_data["win"]/float(len(games)))*100, 2)
        report_data["avg_clues_asked"] = round((report_data["avg_clues_asked"]/float(len(games))), 2)
        report_data["avg_duration"] = round((report_data["avg_duration"] / float(len(games))), 2)
        report_data["has_errors"] = round((report_data["has_errors"]/float(len(games)))*100, 2)
        report_data["warnings"] = round((report_data["warnings"]/float(len(games)))*100, 2)
    except Exception as e:
        print(e)
        report_data['clueitem_most_asked'] = None
        report_data['clueitem_breakdown'] = None
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