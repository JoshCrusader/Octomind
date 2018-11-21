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
from octo_site.db_conf import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from octo_site.reports_controller import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from utils import federate, ajax_helper

from django.http import HttpResponse
from views_func import *
from api_func import *

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

def dashboard(request):
    return render(request,'octo_site/dashboard.html')

def signout(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request,'octo_site/dashboard.html')

def page_sensor(request):
    return page_func.page_sensor(request)

def page_venue(request):
    return page_func.page_venue(request)

def control_panel(request):
    return control_panel_func.control_panel(request)

def view_room(request, game_id):
    print("viewing room")
    return view_room_func.view_room(request, game_id)

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
def get_sensor_by_game(request, game_id):
    data_return = []
    for sensor in Game.objects.get(game_id=game_id).get_sensors_on_trigger_sequence:
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
def get_all_time_data_sensor(request,sensor_id):
    return JsonResponse(Sensor.objects.get(sensor_id=sensor_id).get_all_time_data)

def room_analysis(request):
    return render(request, 'octo_site/reports/room_analysis.html',{"rooms":Room.objects.all()})

def room_details_analysis(request):
    return room_analysis_func.room_details_analysis(request)

def exception_report(request):
    return render(request, 'octo_site/reports/exception_report.html',{"rooms":Room.objects.all()})

def exception_report_details(request):
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
def data_vis(request, room_id):
    room = Room.objects.get(room_id=room_id)
    return render(request, 'octo_site/test_files/data_vis.html', {"room":room, "game":Game.objects.get(game_id=1)})

def data_vis_v2(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room_id)
    return render(request, 'octo_site/test_files/data_vis_v2.html', {"room":room, "game":Game.objects.get(game_id=game_id)})

def live_monitoring(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room.room_id)
    return render(request, 'octo_site/test_files/live_monitoring_data.html', {"room":room, "game":Game.objects.get(game_id=game_id)})

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