from django.shortcuts import render,redirect
from octo_site.models import *
import json
from django.http import HttpResponseRedirect, JsonResponse
from octo_site.forms import *
from django.core import serializers
import socket
import pytz
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User,Group
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import sys
from octo_site.db_conf import *

from octo_site.reports_controller import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from utils import federate, ajax_helper

from django.http import HttpResponse
from views_func import *
from api_func import *
# Create your views here
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
    return render(request, 'octo_site/register.html')
def page_sensor(request):
    if request.method == 'POST':
        print("posted, bitches",request.POST['type'])
        if request.POST['type'] == "sensor":
            add_sensor(request)
        elif request.POST['type'] == "sensor_type":
            add_sensor_type(request)
        elif request.POST['type'] == "rpi":
            add_rpi(request)
        elif request.POST['type'] == "edit_sensor":
            edit_sensor(request)
        elif request.POST['type'] == "edit_sensor_type":
            edit_sensor_type(request)
        elif request.POST['type'] == "edit_rpi":
            edit_rpi(request)
        elif request.POST['type'] == "delete_sensor":
            delete_sensor(request)
        return HttpResponseRedirect(reverse('page_sensor'))
    return render(request, 'octo_site/settings/sensor_page.html',{"sensors":Sensor.objects.all().reverse(),"rooms":Room.objects.all(),"sensor_type":SensorType.objects.all(),"rpi":Rpi.objects.all()})
def page_venue(request):

    if request.method == 'POST':
        if request.POST['type'] == "room":
            add_room(request)
        elif request.POST['type'] == "room_edit":
            edit_room(request)
        elif request.POST['type'] == "room_delete":
            delete_room(request)
        elif request.POST['type'] == "branch":
            add_branch(request)
        elif request.POST['type'] == "branch_edit":
            edit_branch(request)
        elif request.POST['type'] == "branch_delete":
            delete_branch(request)
        return HttpResponseRedirect(reverse('page_venue'))
    return render(request, 'octo_site/settings/venue_page.html',
                  {"branches":Branch.objects.all(),"rooms":Room.objects.all(),"room_form":RoomForm(),"edit_room_form":EditRoomForm()})

def control_panel(request):
    return control_panel_func.control_panel(request)


def view_room(request, game_id):
    return view_room_func.view_room(request, game_id)

def sandbox_analysis(request, room_id):
    return sandbox_analysis_func.sandbox_analysis(request, room_id)

def market_report(request):
    return market_report_func.market_report(request)

def access_room(request):
    ## Add Room in the game room
    if request.method == 'POST':
        pass
# AJAX FUNCTIONS
@csrf_exempt
def update_plot(request):
    width = request.POST['width']
    height = request.POST['height']
    data = request.POST['coords']
    data = json.loads(data)
    print(data)
    print(height,width)
    for dat in data:
        print(dat['id'])
        tCoord = (float(dat['top_coordinate'].replace("px",""))/float(height))*100
        lCoord = (float(dat['left_coordinate'].replace("px",""))/float(width))*100
        sensor = Sensor.objects.get(sensor_id=dat['id'])
        sensor.top_coordinate = round(tCoord, 3)
        sensor.left_coordinate = round(lCoord, 3)
        sensor.save()
        print(sensor.top_coordinate,sensor.left_coordinate)
    return JsonResponse({'filename':"kapiha"})
@csrf_exempt
def upload_process(request):
    return JsonResponse({'filename':"kapiha"})
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
def get_sensor_by_game(request, game_id):
    data_return = []
    for sensor in Game.objects.get(game_id=3).get_sensors_on_trigger_sequence:
        data_return.append({"sensor_id":sensor.sensor_id,"sensor_name": sensor.sensor_name, "phase_name":sensor.phase_name,"top_coordinate": sensor.top_coordinate,"left_coordinate": sensor.left_coordinate,"rpi_id": sensor.rpi_id, "sensor_type_id": sensor.sensor_type_id, "sequence_number": sensor.sequence_number})
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
def all_sensor_data(request):
    data = pull_all_sensor_data()
    for d in data:
        sensor = Sensor.objects.get(sensor_id=d['sensor_id'])
        d['sensor_name'] = sensor.sensor_name
        d['rpi_id'] = sensor.rpi_id
        d['sensor_type_id'] = sensor.sensor_type_id
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
    print("duration",g.get_duration)
    print("clues asked",g.get_num_clues_asked)
    print("is solved",g.is_solved)
    print("has error",g.has_error)
    return JsonResponse({"data": data})
@csrf_exempt
def game_tally(request,game_id):
    g = Game.objects.get(game_id=game_id)
    data = g.pull_game_tally(g)
    return JsonResponse({"data": data})
def dashboard(request):
    return render(request,'octo_site/dashboard.html')
def signout(request):
    logout(request)
    return redirect('index')
def index(request):
    print("gago")
    return render(request,'octo_site/dashboard.html')

@csrf_exempt
def get_cur_games(request):
    return ajax_helper.get_cur_games(request)

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
def add_clue(request):
    return ajax_helper.add_clue(request)

@csrf_exempt
def get_clues_by_game(request,game_id):
    return ajax_helper.get_clues_by_game(game_id)

@csrf_exempt
def get_log_distribution(request, game_ids):
    #must get all logs of each game to plot the sensor distribution between games
    data_return = {}
    gids = game_ids.split("-")
    games = []
    for g in gids:
        games.append(Game.objects.get(id=int(g)))
        data_return[str(g)] = None
    for game in games:
        data = game.pull_data_fr_game(game)

        for d in data:
            if int(d["value"]) == 1:
                data_return[str(game.game_id)].append(d)
    return JsonResponse({"data": data_return})

@csrf_exempt
def get_log_summary(request,game_ids):
    '''
    :param request: 
    :param game_ids: slug of game ids
    :return: returns an average of all the sensor logs
    '''
    summary_ave_data = {}
    data_return = []
    gids = game_ids.split("-")
    games = []

    for g in gids:
        games.append(Game.objects.get(game_id=int(g)))
    for game in games:
        data = game.pull_data_game(game)
        for d in data:
            if int(d["time_solved"]) != 0:
                data_return.append(d)
    sensors = games[0].room.get_all_sensors
    for s in sensors:
        summary_ave_data[s.sensor_id] = {"sensor_id":s.sensor_id, "sensor_name":s.sensor_name, "avg_time_solved":0,"avg_min_stamped":0,"count":0}
    for d in data_return:
        for s in sensors:
            if d["sensor_id"] == s.sensor_id:
                summary_ave_data[s.sensor_id]["avg_time_solved"] += d["time_solved"]
                summary_ave_data[s.sensor_id]["avg_min_stamped"] += d["min_stamped"]
                summary_ave_data[s.sensor_id]["count"] += 1

    for sum_av in summary_ave_data:
        summary_ave_data[sum_av]["avg_time_solved"] = round(summary_ave_data[sum_av]["avg_time_solved"]/summary_ave_data[sum_av]["count"], 2)
        summary_ave_data[sum_av]["avg_min_stamped"] = round(summary_ave_data[sum_av]["avg_min_stamped"]/summary_ave_data[sum_av]["count"], 2)
    print(summary_ave_data)
    return JsonResponse({"data": summary_ave_data})

#TEST URLS
def get_market(request):
    return get_market_func.get_market(request)

def data_vis(request, room_id):
    room = Room.objects.get(room_id=room_id)
    return render(request, 'octo_site/test_files/data_vis.html', {"room":room, "game":Game.objects.get(game_id=1)})

def data_vis_v2(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room_id)
    return render(request, 'octo_site/test_files/data_vis_v2.html', {"room":room, "game":Game.objects.get(game_id=game_id)})

def live_monitoring(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room.room_id)
    return render(request, 'octo_site/test_files/live_monitoring_data.html', {"room":room, "game":Game.objects.get(game_id=game_id)})

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


def add_room(request):
    if RoomForm(request.POST, request.FILES).is_valid():
        room = Room(room_name=request.POST['room_name'], branch_id=request.POST['branch_id'],
                    header_img=request.FILES['header_img'], blueprint_file=request.FILES['blueprint_file'])
        room.save()
def add_branch(request):
    branch = Branch(name=request.POST['name'], address=request.POST['address'])
    branch.save()
def add_sensor(request):
    sensor = Sensor(sensor_name=request.POST['sensor_name'], rpi_id=request.POST['sensor_rpi_id'],
                sensor_type_id=request.POST['sensor_sensor_type_id'],phase_name=request.POST['phase_name'])
    sensor.sequence_number = sensor.get_sequence_number
    sensor.save()
def add_sensor_type(request):
    sensor_type = SensorType(sensor_type_name=request.POST['sensor_type_name'], val_name=request.POST['val_name'],
                trigger_treshold=request.POST['trigger_treshold'])
    sensor_type.save()
def add_rpi(request):
    try:
        socket.inet_aton(request.POST['ip_address'])
        rpi = Rpi(name=request.POST['name'], ip_address=request.POST['ip_address'],
                  room_id=request.POST['room_id'])
        rpi.save()
    except socket.error:
        messages.warning(request, 'IP Address is invalid, please enter another IP.')
def edit_sensor(request):
    sensor = Sensor.objects.get(sensor_id=request.POST['sensor_id'])
    sensor.sensor_name = request.POST['sensor_name']
    sensor.sensor_type_id = request.POST['sensor_sensor_type_id']
    sensor.rpi_id = request.POST['sensor_rpi_id']

    sensor.save()
def edit_room(request):
    room = Room.objects.get(room_id=request.POST['room_id'])
    room.room_name = request.POST['room_name']
    room.branch_id = request.POST['branch_id']
    try:
        sequences = request.POST['game_sequence'].split(",")
        for i,s in enumerate(sequences,1):
            change_sequence =  Sensor.objects.get(sensor_id=int(s))
            print("sensor_id: ", s, "| ctr: ",i)
            change_sequence.sequence_number = i
            change_sequence.save()
    except:
        pass
    room.save()
def edit_branch(request):
    branch = Branch.objects.filter(branch_id=request.POST['branch_id'])[0]
    branch.name = request.POST['name']
    branch.address = request.POST['address']
    branch.save()
def edit_sensor_type(request):
    sensor_type = SensorType.objects.get(sensor_type_id=request.POST['sensor_type_id'])
    sensor_type.sensor_type_name = request.POST['sensor_type_name']
    sensor_type.val_name = request.POST['val_name']
    sensor_type.trigger_treshold = request.POST['trigger_treshold']
    sensor_type.save()
def edit_rpi(request):
    rpi = Rpi.objects.get(rpi_id=request.POST['rpi_id'])
    rpi.name = request.POST['name']
    rpi.ip_address = request.POST['ip_address']
    rpi.room_id = request.POST['room_id']
    rpi.save()
def delete_sensor(request):
    sensor = Sensor.objects.get(sensor_id=request.POST['sensor_id'])
    sensor.delete()
def delete_room(request):
    room = Room.objects.filter(room_id=request.POST['room_id'])
    room.delete()
def delete_branch(request):
    branch = Branch.objects.filter(branch_id=request.POST['branch_id'])
    branch.delete()
def room_analysis(request):
    return render(request, 'octo_site/reports/room_analysis.html',{"rooms":Room.objects.all()})
def room_details_analysis(request):
    report_data=""
    room=""
    msg = ""
    gamedet=""
    games=None

    print("heyout", report_data)
    if request.method == 'POST':
        room = Room.objects.get(room_id=request.POST['room_id'])
        if request.POST['report_cat'] == "range":
            report_data,msg,games = get_range_report(request,room)
        elif request.POST['report_cat'] == "monthly":
            report_data, msg, games = get_monthly_report(request,room)
        elif request.POST['report_cat'] == "yearly":
            report_data, msg, games = get_yearly_report(request,room)
        elif request.POST['report_cat'] == "daily":
            report_data, msg, games = get_daily_report(request,room)
        else:
            print("what")
        print("rep_data", report_data)
    print("bro wtf")
    print("rep_data", report_data)
    return render(request, 'octo_site/reports/details/room_details_analysis.html',{"report_data":report_data,"msg":msg,"games":games,"room":room,"records_len":len(games)})

def sensor_analysis(request):
    return render(request, 'octo_site/reports/sensor_analysis.html')
def trend_analysis(request):
    return render(request, 'octo_site/reports/trend_analysis.html')
def sample_marker(request):
    return render(request, 'octo_site/sample_marker.html')
def game_logs(request):
    utc = pytz.UTC
    cur_games = []
    cur_inds = []
    all_g = Game.objects.all()
    gd = GameDetails.objects.filter(timeend__isnull=True)
    for g in gd:
        diff = datetime.now().replace(tzinfo=utc) - g.timestart.replace(tzinfo=utc)
        days = diff.days
        days_to_hours = days * 24
        diff_btw_two_times = diff.seconds / 3600
        overall_hours = days_to_hours + diff_btw_two_times
        #difference between time and now is less than 1 hour, then it is a past game.
        if diff_btw_two_times < 1:
            cur_games.append(Game.objects.get(game_id=g.game_details_id))
            cur_inds.append(g.game_details_id)
    for ag in all_g:
        if ag.game_id in cur_inds:
            all_g.remove(ag)
    return render(request, 'octo_site/game_logs/game_logs.html', {'games': all_g, 'cur_games': cur_games})
def game_logs_detail(request,game_id):
    g = Game.objects.get(game_id=game_id)
    summary = g.pull_game_summary(g)
    return render(request, 'octo_site/game_logs/game_logs_detail.html',
                  {'game': g,'general_info':summary['general_info'],'sensor_info': summary['sensor_info']})


def analyze_game_logs(request,game_ids):
    gids = game_ids.split("-")
    games = []
    for g in gids:
        games.append(Game.objects.get(game_id=int(g)))
    return render(request, 'octo_site/game_logs/game_logs_analysis.html',
                  {"room_id":games[0].room_id,"room": games[0].room, "id_slugs": game_ids, "game_count":len(games),'game_ids': gids, "games": games})
'''

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

'''

@csrf_exempt
def get_players_data(request):
    data = {}
    return JsonResponse({"data", data})
