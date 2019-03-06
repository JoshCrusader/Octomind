from django.shortcuts import render
from octo_site.models import *
from django.http import HttpResponseRedirect, JsonResponse
import calendar
import json

def get_range_games(request):
    games=[]
    sd = datetime.strptime(request.POST['sd'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['ed'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        games.append(g)
            
    return games
def get_monthly_games(request):
    games = []
    month = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=month.year)

    for det in gamedet:
        if det.timestart.month == month.month:
            g = Game.objects.get(game_id=det.game_details_id)
            games.append(g)
    return games
def get_yearly_games(request):
    games = []
    year = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__year=year.year)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        games.append(g)
    return games
def get_daily_games(request):
    games = []
    sd = datetime.strptime(request.POST['date'] + " 00:00:00", '%Y-%m-%d %H:%M:%S')
    ed = datetime.strptime(request.POST['date'] + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    gamedet = GameDetails.objects.filter(timestart__gte=sd, timestart__lte=ed)
    for det in gamedet:
        g = Game.objects.get(game_id=det.game_details_id)
        games.append(g)
    return games

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def setup_sales(c, data, cur_date, reqsd, reqed):
    stat = 0
    rooms = Room.objects.all()
    if(c == 'yearly'):
        stat = 12
        data['sales']['labels'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    elif(c == 'monthly'):
        month_date = datetime.strptime(cur_date + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        stat = calendar.monthrange(month_date.year, month_date.month)[1]
        data['sales']['labels'] = []
        for i in range(1, stat+1):
            data['sales']['labels'].append(i)
    if(c == 'yearly' or c == 'monthly'):
        for i in range(1, stat+1):
            data['sales'][i] = {}
            data['sales'][i]['count'] = 0
            data['sales'][i]['sales'] = 0
            data['sales'][i]['costs'] = 0
            data['sales'][i]['title'] = i
            for room in rooms:
                data['sales'][i]['roomsales'+str(room.room_id)] = 0
    elif(c == 'range'):
        sd = datetime.strptime(reqsd + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        ed = datetime.strptime(reqed + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        data['sales']['labels'] = []
        for a_date in daterange(sd, ed):
            datekey = str(a_date.year)+'-'+str(a_date.month)+'-'+str(a_date.day)
            data['sales'][datekey] = {}
            data['sales'][datekey]['count'] = 0
            data['sales'][datekey]['sales'] = 0
            data['sales'][datekey]['costs'] = 0
            data['sales'][datekey]['title'] = datekey
            data['sales']['labels'].append(datekey)
            for room in rooms:
                data['sales'][datekey]['roomsales'+str(room.room_id)] = 0

def setup_sales_count(c, data, gamedet, teamlen, price_dict, propr, rooom):
    m = 1
    if(c == 'yearly'):
        m = gamedet.timestart.month
    elif( c == 'monthly'):
        m = gamedet.timestart.day
    else:
        m = str(gamedet.timestart.year)+'-'+str(gamedet.timestart.month)+'-'+str(gamedet.timestart.day)

    if(gamedet.solved == 1):
        sub = gamedet.timeend - gamedet.timestart
        if(sub <= timedelta(minutes = 20)):
            data['costs'] += 150*teamlen
            data['sales'][m]['costs'] += 150*teamlen
            propr['roomdata'][rooom.room_id]['costs'] += 150*teamlen

    data['sales'][m]['count'] += 1
    data['sales'][m]['sales'] += price_dict[teamlen]
    data['sales'][m]['roomsales'+str(rooom.room_id)] += price_dict[teamlen]
    data['totalsales'] += price_dict[teamlen]

def get_game_sales(games, req, propr):
    data = {}
    data['sales'] = {}
    data['sales']['labels'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data['teamcount'] = {}
    data['ages'] = {}
    data['totalsales'] = 0
    data['costs'] = 0
    data['totalsolved'] = 0
    data['totalfailed'] = 0
    data['totalage'] = 0
    data['gendersales'] = [0, 0]
    data['rooms'] = {}

    for i in Room.objects.all():
        data['rooms'][i.room_id] = {}
        data['rooms'][i.room_id]['label'] = i.room_name
        data['rooms'][i.room_id]['sales'] = 0
        data['rooms'][i.room_id]['gendersales'] = [0, 0]
        propr['roomdata'][i.room_id] = {}
        propr['roomdata'][i.room_id]['sales'] = 0
        propr['roomdata'][i.room_id]['costs'] = 0
        propr['roomdata'][i.room_id]['gamelen'] = 0
        propr['roomdata'][i.room_id]['totalsolved'] = 0
        propr['roomdata'][i.room_id]['totalfailed'] = 0

    price_dict = {
        1: 1100,
        2: 1100,
        3: 1500,
        4: 1800,
        5: 2000,
        6: 2400
    }
    solo_dict = {
        1: 1100,
        2: 550,
        3: 500,
        4: 450,
        5: 400,
        6: 400
    }

    age_dict = ['0-17', '18-22', '23-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65', '66+']
    stat = 12

    setup_sales(req.POST['report_cat'], data, req.POST['date'],req.POST['sd'],req.POST['ed'])
    for age_group in age_dict:
        data['ages'][age_group] = {}
        data['ages'][age_group]['count'] = 0
        data['ages'][age_group]['success'] = 0
        data['ages'][age_group]['fail'] = 0
        data['ages'][age_group]['sales'] = 0
        for room in Room.objects.all():
            data['ages'][age_group]['rsales'+str(room.room_id)] = 0

    for i in range(0, 7):
        data['teamcount'][i+1] = {}
        data['teamcount'][i+1]['count'] = 0
        data['teamcount'][i+1]['success'] = 0
        data['teamcount'][i+1]['fail'] = 0

    for game in games:
        gamedet = game.game_details
        solved = gamedet.solved
        m = gamedet.timestart.month
        rooom = game.room
        teams = Teams.objects.filter(game_id = game.game_id)
        teamlen = len(teams)
        if(teamlen == 0):
            teamlen = 1
        data['teamcount'][teamlen]['count'] += 1
        if(solved == 1):
            data['teamcount'][teamlen]['success'] += 1
            data['totalsolved'] += 1
            propr['roomdata'][rooom.room_id]['totalsolved'] += 1
        else:
            data['teamcount'][teamlen]['fail'] += 1
            data['totalfailed'] += 1
            propr['roomdata'][rooom.room_id]['totalfailed'] += 1
            
        setup_sales_count(req.POST['report_cat'], data, gamedet, teamlen, price_dict, propr, rooom)
        data['rooms'][rooom.room_id]['sales'] += price_dict[teamlen]
        propr['roomdata'][rooom.room_id]['sales'] += price_dict[teamlen]
        propr['roomdata'][rooom.room_id]['gamelen'] += 1

        for team in teams:
            player = team.players_players
            age = player.age
            mg = '' ## huhu brute force is life
            if(age >= 0 and age <= 17):
                mg = '0-17'
            elif(age >= 18 and age <= 22):
                mg = '18-22'
            elif(age >= 23 and age <= 30):
                mg = '23-30'
            elif(age >= 31 and age <= 35):
                mg = '31-35'
            elif(age >= 36 and age <= 40):
                mg = '36-40'
            elif(age >= 41 and age <= 45):
                mg = '41-45'
            elif(age >= 46 and age <= 50):
                mg = '46-50'
            elif(age >= 51 and age <= 55):
                mg = '51-55'
            elif(age >= 56 and age <= 60):
                mg = '56-60'
            elif(age >= 61 and age <= 65):
                mg = '61-65'
            else:
                mg = '66+'
            
            if(player.gender == 0):
                data['gendersales'][0] += solo_dict[teamlen]
                data['rooms'][rooom.room_id]['gendersales'][0] += solo_dict[teamlen]
            else:
                data['gendersales'][1] += solo_dict[teamlen]
                data['rooms'][rooom.room_id]['gendersales'][1] += solo_dict[teamlen]

            if(solved == 1):
                data['ages'][mg]['success'] += 1
            else:
                data['ages'][mg]['fail'] += 1

            data['ages'][mg]['rsales'+str(rooom.room_id)] += solo_dict[teamlen]
            data['ages'][mg]['sales'] += solo_dict[teamlen]
            data['ages'][mg]['count'] += 1
            data['totalage'] += 1


    return data

def player_analysis_report(request):
    games = []
    if(request.method == 'POST'):
        if request.POST['report_cat'] == "range":
            games = get_range_games(request)
        elif request.POST['report_cat'] == "monthly":
            games = get_monthly_games(request)
        elif request.POST['report_cat'] == "yearly":
            games = get_yearly_games(request)
        elif request.POST['report_cat'] == "daily":
            games = get_daily_games(request)
        else:
            print("what")
        print(request.POST)
    
    
    properties = {}
    properties['roomdata'] = {}
    detobj = get_game_sales(games, request, properties)
    properties['sales_graph'] = json.dumps(detobj)
    properties['totalsales'] = detobj['totalsales']
    properties['totalcosts'] = detobj['costs']
    properties['agedict'] = detobj['ages']
    properties['totalage'] = detobj['totalage']
    properties['totalsolved'] = detobj['totalsolved']
    properties['totalfailed'] = detobj['totalfailed']
    properties['lengames'] = len(games)
    properties['rooms'] = Room.objects.all()
    return render(request, 'octo_site/reports/market/player_analysis_report/prototype.html', properties)