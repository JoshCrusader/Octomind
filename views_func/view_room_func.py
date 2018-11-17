from django.utils import timezone
from django.shortcuts import render,redirect
from octo_site.models import *
import json

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
            clues = Clues.objects.filter(game_id = game.game_id)
            properties = {}
            properties['gameid'] = game.game_id
            properties['details'] = details
            properties['players'] = players
            properties['clues'] = clues
            room_obj = Room.objects.get(room_id = game.room_id)
            properties['roomid'] = room_obj.room_id
            properties['img'] = room_obj.header_img
            properties['roomname'] = room_obj.room_name
            properties['matchid'] = game.match_id
            properties['blueprint'] = room_obj.blueprint_file
            properties['sensors'] = []
            for sensor in room_obj.get_all_sensors:
                properties['sensors'].append({"sensor_id":sensor.sensor_id,"sensor_name": sensor.sensor_name, "top_coordinate": sensor.top_coordinate,"left_coordinate": sensor.left_coordinate,"rpi_id": sensor.rpi_id, "sensor_type_id": sensor.sensor_type_id, "sequence_number": sensor.sequence_number})
            
            # sensors = Sensor.objects.get(room_id = room_obj.room_id)
            # for i in sensors:
            #     pass
            now_datetime = timezone.now()
            properties['timeend'] = details.timestart + timezone.timedelta(hours=1)+ timezone.timedelta(minutes=1)
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