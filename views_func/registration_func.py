from django.utils import timezone
from django.shortcuts import render
from octo_site.models import *
import json

def registration(request):
    properties = {}
    if(request.method == 'POST'):
        # supr = request.POST['supervisor']
        keeperid = 1
        rid = int(request.POST['room'])
        nomem = int(request.POST['membs'])
        teamname = request.POST['teamname']
        howuknow = request.POST['howuknow']
        gamedets = GameDetails(teamname = teamname, solved = 0)
        gamedets.save()
        game = Game(room_id = rid, game_details_id = gamedets.game_details_id, game_keeper_id = keeperid)
        game.save()
        for i in range(1, nomem+1):
            stri = str(i)
            fname = request.POST['fname'+stri]
            lname = request.POST['lname'+stri]
            email = request.POST['email'+stri]
            cnumber = request.POST['cnumber'+stri]
            firsttime = request.POST['firsttime'+stri]
            loc = request.POST['loc'+stri]
            age = request.POST['age'+stri]
            gender = request.POST['gender'+stri]
            players = Players(firstname = fname, lastname = lname, contact = cnumber, gender = int(gender), email = email, age = int(age), loc_dictionary_id = int(loc))
            players.save()
            teams = Teams(game_id = game.game_id, players_players_id = players.players_id)
            teams.save()
        return render(request,'octo_site/registration/thankyou.html', properties)
    else:
        properties = {}
        properties['locs'] = LocDictionary.objects.all()
        properties['rooms'] = Room.objects.all()
        return render(request,'octo_site/registration/registration.html', properties)