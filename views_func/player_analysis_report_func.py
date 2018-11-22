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
            data['sales'][i]['title'] = i
    elif(c == 'range'):
        sd = datetime.strptime(reqsd + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        ed = datetime.strptime(reqed + " 00:00:00", '%Y-%m-%d %H:%M:%S')
        data['sales']['labels'] = []
        for a_date in daterange(sd, ed):
            datekey = str(a_date.year)+'-'+str(a_date.month)+'-'+str(a_date.day)
            data['sales'][datekey] = {}
            data['sales'][datekey]['count'] = 0
            data['sales'][datekey]['sales'] = 0
            data['sales'][datekey]['title'] = datekey
            data['sales']['labels'].append(datekey)

def setup_sales_count(c, data, gamedet, teamlen, price_dict):
    m = 1
    if(c == 'yearly'):
        m = gamedet.timestart.month
    elif( c == 'monthly'):
        m = gamedet.timestart.day
    else:
        m = str(gamedet.timestart.year)+'-'+str(gamedet.timestart.month)+'-'+str(gamedet.timestart.day)
    data['sales'][m]['count'] += 1
    data['sales'][m]['sales'] += price_dict[teamlen]

def get_game_sales(games, req):
    data = {}
    data['sales'] = {}
    data['sales']['labels'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data['teamcount'] = {}
    data['ages'] = {}
    price_dict = {
        1: 1100,
        2: 1100,
        3: 1500,
        4: 1800,
        5: 2000,
        6: 2400
    }
    age_dict = ['0-17', '18-22', '23-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65', '66+']
    stat = 12

    setup_sales(req.POST['report_cat'], data, req.POST['date'],req.POST['sd'],req.POST['ed'])
    for age_group in age_dict:
        data['ages'][age_group] = {}
        data['ages'][age_group]['count'] = 0
        data['ages'][age_group]['success'] = 0
        data['ages'][age_group]['fail'] = 0

    for i in range(0, 7):
        data['teamcount'][i+1] = {}
        data['teamcount'][i+1]['count'] = 0
        data['teamcount'][i+1]['success'] = 0
        data['teamcount'][i+1]['fail'] = 0

    for game in games:
        gamedet = game.game_details
        solved = gamedet.solved
        m = gamedet.timestart.month
        teams = Teams.objects.filter(game_id = game.game_id)
        teamlen = len(teams)
        if(teamlen == 0):
            teamlen = 1
        data['teamcount'][teamlen]['count'] += 1
        if(solved == 1):
            data['teamcount'][teamlen]['success'] += 1
        else:
            data['teamcount'][teamlen]['fail'] += 1
            
        setup_sales_count(req.POST['report_cat'], data, gamedet, teamlen, price_dict)
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
            
            data['ages'][mg]['count'] += 1
            if(solved == 1):
                data['ages'][mg]['success'] += 1
            else:
                data['ages'][mg]['fail'] += 1

            data['ages'][mg]['count'] += 1


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
    properties['sales_graph'] = json.dumps(get_game_sales(games, request))
    return render(request, 'octo_site/reports/market/player_analysis_report/main.html', properties)