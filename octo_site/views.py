from django.shortcuts import render,redirect
from octo_site.models import *
import json
from django.http import HttpResponseRedirect, JsonResponse
from octo_site.forms import *
from django.core import serializers
import socket
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
    if request.method == 'GET':
        # federate.sync()
        game_details = []
        now_datetime = timezone.now() + timezone.timedelta(hours=8)
        finish_time = now_datetime - timezone.timedelta(hours = 1)
        print(now_datetime)
        for i in GameDetails.objects.all().filter(timestart__gte = finish_time).filter(timeend__isnull = True):
            game_details.append(i)
        games = {}
        for g_d in game_details:
            i = Game.objects.get(game_details_id = g_d.game_details_id)
            games[i.room_id] = {}
            games[i.room_id]['game_id'] = i.game_id
            games[i.room_id]['game'] = (Room.objects.get(room_id = i.room_id))
            ## GETTING TIME DETAILS
            game_detail = GameDetails.objects.get(game_details_id = i.game_details_id)
            games[i.room_id]['minutes'] = (game_detail.timestart + timezone.timedelta(hours = 1) - now_datetime).seconds//60
            games[i.room_id]['seconds'] = (game_detail.timestart + timezone.timedelta(hours = 1) - now_datetime).seconds%60
            ## GETTING PLAYERS DETAILS
            teams = Teams.objects.filter(game_id = i.game_id)
            games[i.room_id]['players'] = []
            for team in teams:
                games[i.room_id]['players'].append(Players.objects.get(players_id = team.players_players_id))
            ## CLUES
            clues = Clues.objects.filter(games_id = i.game_id)
            games[i.room_id]['clues'] = range(0, 3-len(clues))
            games[i.room_id]['mystery'] = range(0, len(clues))
            print(len(clues))
        #for i in games[3]['players']:
        #    print(i.firstname)
        properties = {}
        properties['h'] = 5
        properties['rooms'] = Room.objects.all()
        properties['games'] = games
        return render(request,'octo_site/control_panel.html', properties)
        pass

def view_room(request, game_id):
    try:
        game = Game.objects.get(game_id = game_id)
        if(game is not None):
            details = GameDetails.objects.get(game_details_id = game.game_details_id)
            team = Teams.objects.filter(game_id = game.game_id)
            players = []
            for i in team:
                pass
                players.append(Players.objects.get(players_id = i.players_players_id))
            clues = Clues.objects.filter(games_id = game.game_id)
            properties = {}
            properties['gameid'] = game.game_id
            properties['details'] = details
            properties['players'] = players
            properties['clues'] = clues
            room_obj = Room.objects.get(room_id = game.room_id)
            properties['roomid'] = room_obj.room_id
            properties['img'] = room_obj.header_img
            properties['roomname'] = room_obj.room_name
            properties['blueprint'] = room_obj.blueprint_file
            properties['sensors'] = []
            for sensor in room_obj.get_all_sensors:
                properties['sensors'].append({"sensor_id":sensor.sensor_id,"sensor_name": sensor.sensor_name, "top_coordinate": sensor.top_coordinate,"left_coordinate": sensor.left_coordinate,"rpi_id": sensor.rpi_id, "sensor_type_id": sensor.sensor_type_id, "sequence_number": sensor.sequence_number})
            
            # sensors = Sensor.objects.get(room_id = room_obj.room_id)
            # for i in sensors:
            #     pass
            now_datetime = timezone.now() + timezone.timedelta(hours=8)
            if(details.timestart + timezone.timedelta(hours=1) > now_datetime):
                properties['done'] = False
                properties['minutes'] = (details.timestart + timezone.timedelta(hours=1) - now_datetime).seconds // 60
                properties['seconds'] = (details.timestart + timezone.timedelta(hours=1) - now_datetime).seconds % 60
            else:
                properties['done'] = True

            if(details.timeend is not None):
                properties['done'] = True
            # print('MINUTES: ')
            # print((details.timestart + timezone.timedelta(hours=1)- now_datetime))
            # print((details.timestart + timezone.timedelta(hours=1) - now_datetime).seconds // 60)
            return render(request,'octo_site/view_room.html', properties)
        else:
            pass
    except Exception as e:
        print(e)
        return render(request,'octo_site/dashboard.html')

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
def sensor_data(request,game_id):
    data = pull_data_live_control_panel(game_id)
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

def data_vis(request, room_id):
    room = Room.objects.get(room_id=room_id)
    return render(request,'octo_site/data_vis.html',{"room":room,"game":Game.objects.get(game_id=1)})

def data_vis_v2(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room_id)
    return render(request,'octo_site/data_vis_v2.html',{"room":room,"game":Game.objects.get(game_id=game_id)})
def live_monitoring(request, game_id):
    room = Room.objects.get(room_id=Game.objects.get(game_id=game_id).room.room_id)
    return render(request,'octo_site/live_monitoring_data.html',{"room":room,"game":Game.objects.get(game_id=game_id)})
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
                sensor_type_id=request.POST['sensor_sensor_type_id'])
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
