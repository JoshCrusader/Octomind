from django.shortcuts import render,redirect
from octo_site.models import *
import json
from django.http import HttpResponseRedirect, JsonResponse
from octo_site.forms import *
from django.core import serializers
import pytz
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import sys
import os
from django.conf import settings
from octo_site.db_conf import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from octo_site.reports_controller import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from utils import federate, ajax_helper,sensor_deebs_popu,script_helper, populatestart, populate_details

from django.http import HttpResponse
from views_func import *
from api_func import *
import random
def handler404(request, template_name="octo_site/handler404.html"):
    response = render_to_response(template_name)
    response.status_code = 404

    return render(request,template_name)

def log_in(request):
    user = None
    try:
        user = authenticate(username=request.POST['user'], password=request.POST['password'])
    except:
        None
    if request.method == 'POST':
        if user is not None:
            request.session['username'] = user.username
            request.session['guest'] = True
            request.session['logged'] = True
            login(request, user)
        else:
            messages.warning(request,'Wrong credentials, please try again.')
        return redirect('index')
    else:
        return render(request, 'octo_site/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        usertype = request.POST.get('usertype')
        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname)

        if usertype == "os":
            group = Group.objects.get(name="Operations Supervisor")
            user.groups.add(group)
        elif usertype == "gk":
            group = Group.objects.get(name="Gamekeeper")
            user.groups.add(group)
        elif usertype == "own":
            group = Group.objects.get(name="Owner")
            user.groups.add(group)

        user.save()
        messages.warning(request, 'Account Created.')
        return redirect('index')
    return render(request, 'octo_site/user_module/register.html', {'branches':Branch.objects.all()})

def list_user(request):
    return render(request, 'octo_site/user_module/list_user.html',{'users':User.objects.all()})

def registration(request):
    return registration_func.registration(request)

def dashboard(request):
    return render(request,'octo_site/dashboard.html')

def signout(request):
    logout(request)
    return redirect('index')

def index(request):
    return redirect('control_panel')
    #return render(request,'octo_site/dashboard.html')

def page_sensor(request):
    return page_func.page_sensor(request)

def page_venue(request):
    return page_func.page_venue(request)

def control_panel(request):
    return control_panel_func.control_panel(request)

def view_room(request, game_id):
    print("viewing room")
    return view_room_func.view_room(request, game_id)

def tv_monitor(request, game_id):
    return tv_monitor_func.tv_monitor(request, game_id)
def sandbox_analysis(request, room_id):
    return sandbox_analysis_func.sandbox_analysis(request, room_id)

def market_report(request):
    return market_report_func.market_report(request)

def map_market_report(request):
    return render(request, 'octo_site/reports/market_map.html')

def player_analysis_report(request):
    return player_analysis_report_func.player_analysis_report(request)

def market_analysis(request):
    return market_analysis_func.market_analysis(request)
    
def access_room(request):
    ## Add Room in the game room
    if request.method == 'POST':
        pass
# AJAX FUNCTIONS
@csrf_exempt
def get_game_duration(request,game_id):
    game = Game.objects.get(game_id=game_id)
    return JsonResponse({"duration":game.get_duration,"final_duration":game.get_final_duration})
@csrf_exempt
def update_plot(request):
    return plot_func.update_plot(request)
@csrf_exempt
def get_room_by_room_id(request,room_id):
    room = Room.objects.get(room_id=room_id)
    return JsonResponse({"room_id":room.room_id,"room_name":room.room_name,"header_img":str(room.header_img),"blueprint_file":str(room.blueprint_file)})
@csrf_exempt
def get_sensors_by_room_id(request,room_id):
    data_return = []
    for sensor in Room.objects.get(room_id=room_id).get_all_sensors:
        data_return.append({"sensor_id":sensor.sensor_id,"sensor_name": sensor.sensor_name, "top_coordinate": sensor.top_coordinate,"left_coordinate": sensor.left_coordinate,"rpi_id": sensor.rpi_id, "sensor_type_id": sensor.sensor_type_id, "sequence_number": sensor.sequence_number})
    return JsonResponse({"sensors":data_return})
@csrf_exempt
def get_clues_list_by_room(request,room_id):
    data_return = []
    for clue_item in ClueItem.objects.filter(room_id=room_id):
        data_return.append({"detail":clue_item.detail})
    return JsonResponse({"items":data_return})
@csrf_exempt
def get_sensor_by_game(request, game_id):
    data_return = []
    for sensor in Game.objects.get(game_id=game_id).get_sensors_on_trigger_sequence:
        data_return.append({"sensor_id":sensor.sensor_id,
                            "sensor_name": sensor.sensor_name,
                            "phase_name":sensor.phase_name})
    return JsonResponse({"sensors":data_return})
@csrf_exempt
def sensor_data(request,game_id):
    data = pull_data_live_control_panel(game_id)
    for d in data:
        sensor = Sensor.objects.get(sensor_id=d['sensor_id'])
        d['sensor_name'] = sensor.sensor_name
        d['rpi_id'] = sensor.rpi_id
        d['sensor_type_id'] = sensor.sensor_type_id
    return JsonResponse({"data": data})

@csrf_exempt
def get_cur_phase(request, game_id):
    return JsonResponse({"phase": Game.objects.get(game_id=game_id).get_current_phase})
@csrf_exempt
def all_sensor_data(request):
    data = pull_all_sensor_data()
    for d in data:
        sensor = Sensor.objects.get(sensor_id=d['sensor_id'])
        d['sensor_name'] = sensor.sensor_name
        d['rpi_id'] = sensor.rpi_id
        d['sensor_type_id'] = sensor.sensor_type_id
    return JsonResponse({"data": data})

@csrf_exempt
def select_sensor_data(request, game_ids):
    data = []
    gids = game_ids.split("-")
    for g in gids:
        game = Game.objects.get(game_id=g)
        game_data = game.pull_data_fr_game(game)
        for gd in game_data:
            data.append(gd)
    return JsonResponse({"data": data})

@csrf_exempt
def game_cur_logs(request,game_id):
    g = Game.objects.get(game_id=game_id)
    data = g.pull_data_game(g)
    return JsonResponse({"data": data})
@csrf_exempt
def game_summary(request,game_id):
    g = Game.objects.get(game_id=game_id)
    data = g.pull_game_summary(g)
    return JsonResponse({"data": data})
@csrf_exempt
def game_tally(request,game_id):
    g = Game.objects.get(game_id=game_id)
    data = g.pull_game_tally(g)
    return JsonResponse({"data": data})

@csrf_exempt
def get_cur_games(request):
    return ajax_helper.get_cur_games(request)

@csrf_exempt
def get_clue_data(request,game_id):
    return JsonResponse({"data": Game.objects.get(game_id=game_id).get_data_clues})

@csrf_exempt
def get_player_list(request):
    return ajax_helper.get_player_list(request)

@csrf_exempt
def start_game(request):
    return ajax_helper.start_game(request)

@csrf_exempt
def end_game(request):
    return ajax_helper.end_game(request)
@csrf_exempt
def confirm_end_game(request):
    return ajax_helper.confirm_end_game(request)

@csrf_exempt
def add_clue(request):
    return ajax_helper.add_clue(request)

@csrf_exempt
def get_clues_by_game(request,game_id):
    return ajax_helper.get_clues_by_game(game_id)

@csrf_exempt
def get_log_distribution(request, game_ids):
    return plot_func.get_log_distribution(request,game_ids)

@csrf_exempt
def get_log_summary(request,game_ids):
    return plot_func.get_log_summary(request, game_ids)

@csrf_exempt
def get_market(request):
    return get_market_func.get_market(request)

@csrf_exempt
def get_room_market(request):
    return get_room_market_func.get_room_market(request)

@csrf_exempt
def get_all_time_data(request,room_id):
    return JsonResponse(Room.objects.get(room_id=room_id).get_all_time_data)

@csrf_exempt
def get_all_time_data_sensor(request,sensor_id):
    return JsonResponse(Sensor.objects.get(sensor_id=sensor_id).get_all_time_data)

@csrf_exempt
def get_exception_data(request):
    return get_exception_report.get_exception_data(request)
@csrf_exempt
def open_notif(request):
    notifs = Notifs.objects.all()
    for n in notifs:
        n.viewed = 1
        n.save()
    return JsonResponse({"data": 'ok'})
@csrf_exempt
def check_notif(request):
    notifs = Notifs.objects.all().order_by("-timestamp")[0:5]
    chk = Notifs.check_new_notif()
    data=[]
    for n in notifs:
        data.append({"new_notif":chk,"details":n.details,"timestamp":n.get_time_ago,"game_id":n.game_id,"is_ongoing":n.game.is_ongoing})
    return JsonResponse({"data": data})
@csrf_exempt
def get_all_time_data_sensor(request,sensor_id):
    return JsonResponse(Sensor.objects.get(sensor_id=sensor_id).get_all_time_data)

def room_analysis(request):
    return render(request, 'octo_site/reports/room_analysis.html',{"rooms":Room.objects.all()})

def room_details_analysis(request):
    return room_analysis_func.room_details_analysis(request)

def exception_report(request):
    return render(request, 'octo_site/reports/exception_report.html',{"rooms":Room.objects.all()})

def exception_report_details(request):
    print("wat happening")
    return exception_report_func.exception_report_details(request)

def sensor_analysis(request):
    return render(request, 'octo_site/reports/sensor_analysis.html')

def trend_analysis(request):
    return render(request, 'octo_site/reports/trend_analysis.html')

def sample_marker(request):
    return render(request, 'octo_site/sample_marker.html')

def game_logs(request):

    return game_logs_func.game_logs(request)

def game_logs_detail(request,game_id):
    return game_logs_func.game_logs_detail(request,game_id)

def analyze_game_logs(request,game_ids):
    return game_logs_func.analyze_game_logs(request,game_ids)

@csrf_exempt
def get_players_data(request):
    data = {}
    return JsonResponse({"data", data})

###### TEST URLS ######
def data_vis(request):
    print("populating")
    sensor_deebs_popu.main_start()
    return render(request, 'octo_site/test_files/population.html')

def data_vis_v2(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room_id)
    return render(request, 'octo_site/test_files/data_vis_v2.html', {"room":room, "game":Game.objects.get(game_id=game_id)})

def live_monitoring(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room.room_id)
    return render(request, 'octo_site/test_files/live_monitoring_data.html', {"room":room, "game":Game.objects.get(game_id=game_id)})

def live_monitoring_iot(request):
    timestart=datetime.now()
    room = Room.objects.get(room_id=2)
    return render(request, 'octo_site/test_files/iot/live_monitoring_data.html',{"timestart":timestart})
@csrf_exempt
def sensor_data_iot(request,timestart):
    date = timestart.split("_")[0]
    time = timestart.split("_")[1]
    time = time.replace("-",":")
    st = date + " " + time
    print(st)
    array = []
    data = pull_data_live_control_panel_iot()
    return JsonResponse({"data": data})

def log_percentage_complete(request, game_ids):
    gids = game_ids.split("-")
    games = []
    for g in gids:
        games.append(Game.objects.get(game_id=int(g)))
    return render(request, 'octo_site/test_files/log_distribution.html', {"room":games[0].room,"id_slugs":game_ids,'game_ids':gids,"games": games})

def log_distribution(request, game_ids):
    gids = game_ids.split("-")
    games = []
    for g in gids:
        games.append(Game.objects.get(game_id=int(g)))
    return render(request, 'octo_site/test_files/log_distribution.html', {"room":games[0].room,"id_slugs":game_ids,'game_ids':gids,"games": games})

def log_summary(request, game_ids):
    gids = game_ids.split("-")
    games = []
    for g in gids:
        games.append(Game.objects.get(game_id=int(g)))
    return render(request, 'octo_site/test_files/log_summary.html', {"room":games[0].room,"id_slugs":game_ids,'game_ids':gids,"games": games})
######


def script_helper_v(request):
        return render(request, 'octo_site/script_enhancer.html')
@csrf_exempt
def add_mins(request):
    return script_helper.add_mins(request)
@csrf_exempt
def add_script_logs(request):
    print("scripts are being added to game ",request.POST['gid'])
    game = Game.objects.get(game_id=request.POST['gid'])
    sensors = game.room.get_all_sensors
    division = round(60/len(sensors),2)
    cum_time = 0
    for s in sensors:
        insert_val(s.sensor_id, game.game_details.timestart, 0)
    if request.POST['case_num'] == '1':
        for s in sensors:
            cum_time += gen_r_random(6, division)
            ts = game.game_details.timestart + timedelta(minutes=cum_time, seconds=math.ceil(random.random() * 59))
            insert_val(s.sensor_id,ts,1)
    elif request.POST['case_num'] == '2':
        for i,s in enumerate(sensors):
            cur_s = s
            if i == 0:
                cur_s = sensors[1]
            elif i == 1:
                cur_s = sensors[0]
            cum_time += gen_r_random(6, division)
            ts = game.game_details.timestart + timedelta(minutes=cum_time, seconds=math.ceil(random.random() * 59))
            insert_val(cur_s.sensor_id,ts,1)
    elif request.POST['case_num'] == '3':
        sensor_deducted = sensors[:-1]
        for s in sensor_deducted:
            cum_time += gen_r_random(6, division)
            ts = game.game_details.timestart + timedelta(minutes=cum_time, seconds=math.ceil(random.random() * 59))
            insert_val(s.sensor_id,ts,1)
    elif request.POST['case_num'] == '4':
        sensor_deducted = sensors[:-2]
        for s in sensor_deducted:
            cum_time += gen_r_random(5, division*1.45)
            ts = game.game_details.timestart + timedelta(minutes=cum_time, seconds=math.ceil(random.random() * 59))
            insert_val(s.sensor_id, ts, 1)
    return JsonResponse({"response":'logs are inserted'})
@csrf_exempt
def add_script_clue(request):
    game = Game.objects.get(game_id=request.POST['gid'])
    delta_time = timedelta(minutes=int(request.POST['min']), seconds=math.ceil(random.random() * 59))



    citem = ClueItem.objects.get(id=request.POST['ci_id'])

    cd = ClueDetails(detail=citem.detail, timestamp=game.game_details.timestart + delta_time)
    cd.save()

    clue = Clues(clue_details_id=cd.clue_details_id, game_id=game.game_id)
    clue.save()

    citem_detail = ClueItemDetails(clue_id=clue.clue_id, clue_item_id=citem.id)
    citem_detail.save()
    return JsonResponse({"response":'clue added'})
@csrf_exempt
def set_end_time(request):
    game = GameDetails.objects.get(game_details_id=request.POST['gid'])
    delta_time = timedelta(minutes=int(request.POST['min']), seconds=math.ceil(random.random() * 59))
    game.timeend = game.timestart + delta_time
    game.save()
    print(game.timeend)
    return JsonResponse({"response":'end time setted'})
def gen_r_random(x, y):
    return x + math.ceil(random.random() * (y - x))

def insert_val(sid,ts,val):
    print("hinserting")
    ts = str(ts.strftime("%Y-%m-%d %H:%M:%S"))
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="sensorDB")
    x = conn.cursor()
    try:
        x.execute("INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);", (sid, ts, val))
        conn.commit()

        print("executed")
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()
    return None

def popstart(request):
    populatestart.popu_start()
    return JsonResponse({"response":'end time setted'})

def pophim(request):
    populate_details.main_start()
    return JsonResponse({"response":'end time setted'})