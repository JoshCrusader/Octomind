from django.shortcuts import render

from octo_site.models import *
from octo_site.db_conf import *
import math
import random
from datetime import datetime,timedelta
import dateutil.relativedelta as relativedelta
def gk_dashboard(request):
    all_g = Game.objects.filter(game_details__timestart__isnull=False)
    games = []
    cur_date_str = datetime.today().strftime('%b %d, %Y')
    date = datetime.today().strftime('%Y-%m-%d')
    yesterdate = datetime.strftime(datetime.today() - timedelta(1), '%Y-%m-%d')
    cur_branch = EmployeeBranch.get_branch(request.user.id)
    unstarted_games_arr = []
    unstarted_games = Game.objects.filter(game_details__timestart__isnull=True)
    for g in reversed(all_g):
        if len(games) >= 5:
            break
        if cur_branch.branch_id == g.room.branch_id:
            games.append(g)
    for gg in reversed(unstarted_games):
        if len(unstarted_games_arr) >= 5:
            break
        if cur_branch.branch_id == gg.room.branch_id:
            unstarted_games_arr.append(gg)

    #computing for the metric above
    metrics = {}
    metrics['total_games'] = len(cur_branch.get_games_on_date(cur_branch,date,"daily",None))
    metrics['comp_total_games'] = metrics['total_games'] - len(cur_branch.get_games_on_date(cur_branch,yesterdate,"daily",None))
    metrics['abs_total_games'] = abs(metrics['comp_total_games'])

    metrics['total_errors'] = len(cur_branch.get_errors_on_date(cur_branch,date,"daily",None))
    metrics['comp_total_errors'] = metrics['total_errors'] - len(cur_branch.get_errors_on_date(cur_branch,yesterdate,"daily",None))
    metrics['abs_total_errors'] = abs(metrics['comp_total_errors'])

    metrics['total_warnings'] = len(cur_branch.get_warnings_on_date(cur_branch,date,"daily",None))
    metrics['comp_total_warnings'] = metrics['total_warnings'] - len(cur_branch.get_warnings_on_date(cur_branch,yesterdate,"daily",None))
    metrics['abs_total_warnings'] = abs(metrics['comp_total_warnings'])
    return render(request, 'octo_site/dashboards/gk_dashboard.html',
                  {'games': games, 'acts': Notifs.get_all_notifs_in_branch(cur_branch.branch_id),
                   'unst_games': unstarted_games_arr, 'metrics':metrics,
                   'branch': cur_branch, 'cur_date': cur_date_str})
def os_dashboard(request):
    yesterdate = datetime.strftime(datetime.today() - timedelta(7), '%Y-%m-%d')
    cur_date_str = datetime.today().strftime('%b %d, %Y')
    date = datetime.today().strftime('%Y-%m-%d')
    cur_branch = EmployeeBranch.get_branch(request.user.id)
    games = cur_branch.get_games_on_date(cur_branch, date, "weekly",None)
    retentions = cur_branch.get_retentions_on_date(cur_branch, date, "weekly",None)
    warnings = cur_branch.get_warnings_on_date(cur_branch, date, "weekly",None)
    errors = cur_branch.get_errors_on_date(cur_branch, date, "weekly",None)
    rooms = Room.objects.filter(branch_id=cur_branch.branch_id)


    #computing chart data
    game_played_chart = []
    room_retentions = []
    anomalies_detected =[]
    sales_per_weekday = []

    for r in rooms:
        game_played_chart.append({'room_name':r.room_name,'games_played':len(games.filter(room_id=r.room_id))})
        room_retentions.append({'room_name': r.room_name,'retaining_customers': cur_branch.get_retentions_on_date(cur_branch, date, "weekly",r.room_id)})
        anomalies_detected.append({'room_name': r.room_name,'anomaly_count':len(errors.filter(game__room_id=r.room_id)) + len(warnings.filter(game__room_id=r.room_id))})
        sales_per_weekday.append({'room_name':r.room_name,'week_data':cur_branch.get_sales_on_date(cur_branch, date, "weekly",r.room_id)})
    # computing for the metric above
    metrics = {}
    metrics['total_games'] = len(games)
    metrics['comp_total_games'] = metrics['total_games'] - len(
        cur_branch.get_games_on_date(cur_branch, yesterdate, "weekly",None))
    metrics['abs_total_games'] = abs(metrics['comp_total_games'])

    metrics['total_errors'] = len(errors)
    metrics['comp_total_errors'] = metrics['total_errors'] - len(
        cur_branch.get_errors_on_date(cur_branch, yesterdate, "weekly",None))
    metrics['abs_total_errors'] = abs(metrics['comp_total_errors'])

    metrics['total_warnings'] = len(warnings)
    metrics['comp_total_warnings'] = metrics['total_warnings'] - len(
        cur_branch.get_warnings_on_date(cur_branch, yesterdate, "weekly",None))
    metrics['abs_total_warnings'] = abs(metrics['comp_total_warnings'])

    metrics['total_anomalies'] = metrics['total_errors'] + metrics['total_warnings']
    metrics['comp_total_anomalies'] = metrics['total_anomalies'] - (
        metrics['total_errors']+metrics['total_warnings'])
    metrics['abs_total_anomalies'] = abs(metrics['comp_total_anomalies'])

    metrics['total_retentions'] = retentions[0]
    metrics['comp_total_retentions'] = metrics['total_retentions'] - cur_branch.get_retentions_on_date(cur_branch, yesterdate, "weekly",None)[0]
    metrics['abs_total_retentions'] = abs(metrics['comp_total_retentions'])

    print("sales",sales_per_weekday)
    return render(request, 'octo_site/dashboards/os_dashboard.html',
                  {'games': games,'metrics':metrics,
                   'games_played_chart':game_played_chart,
                   'room_retentions':room_retentions,
                   'anomalies_detected':anomalies_detected,
                   'sales_per_weekday':sales_per_weekday,
                   'branch':cur_branch,'cur_date':cur_date_str})
def own_dashboard(request):
    yesterdate = datetime.today() - relativedelta.relativedelta(months=1)

    cur_date_str = datetime.today().strftime('%b %d, %Y')
    date = datetime.today().strftime('%Y-%m-%d')
    cur_branch = Branch()
    clues = Clues.objects.all()[:10]  # dummy val
    games = cur_branch.get_games_on_date(None, date, "monthly", None)
    warnings = cur_branch.get_warnings_on_date(None, date, "monthly", None)
    errors = cur_branch.get_errors_on_date(None, date, "monthly", None)
    #rooms = Room.objects.filter(branch_id=cur_branch.branch_id)
    # computing chart data
    room_retentions = []
    sales_per_branch = cur_branch.get_sales_on_date(None, date, "monthly", "all")
    '''
    for r in rooms:
        game_played_chart.append({'room_name': r.room_name, 'games_played': len(games.filter(room_id=r.room_id))})
        room_retentions.append({'room_name': r.room_name,
                                'retaining_customers': cur_branch.get_retentions_on_date(cur_branch, date, "weekly",
                                                                                         r.room_id)})
        anomalies_detected.append({'room_name': r.room_name,
                                   'anomaly_count': len(errors.filter(game__room_id=r.room_id)) + len(
                                       warnings.filter(game__room_id=r.room_id))})
        sales_per_weekday.append({'room_name': r.room_name,
                                  'week_data': cur_branch.get_sales_on_date(cur_branch, date, "weekly", r.room_id)})
    # computing for the metric above
    '''
    metrics = {}
    metrics['total_games'] = len(games)
    metrics['comp_total_games'] = metrics['total_games'] - len(
        cur_branch.get_games_on_date(None, yesterdate, "monthly", None))
    metrics['abs_total_games'] = abs(metrics['comp_total_games'])

    metrics['total_errors'] = len(errors)
    metrics['comp_total_errors'] = metrics['total_errors'] - len(
        cur_branch.get_errors_on_date(None, yesterdate, "monthly", None))
    metrics['abs_total_errors'] = abs(metrics['comp_total_errors'])

    metrics['total_warnings'] = len(warnings)
    metrics['comp_total_warnings'] = metrics['total_warnings'] - len(
        cur_branch.get_warnings_on_date(None, yesterdate, "monthly", None))
    metrics['abs_total_warnings'] = abs(metrics['comp_total_warnings'])

    metrics['total_anomalies'] = metrics['total_errors'] + metrics['total_warnings']
    metrics['comp_total_anomalies'] = metrics['total_anomalies'] - (
        metrics['total_errors'] + metrics['total_warnings'])
    metrics['abs_total_anomalies'] = abs(metrics['comp_total_anomalies'])

    metrics['total_sales'] = cur_branch.get_sales_on_date(None, date, "monthly", None)
    metrics['comp_total_sales'] = metrics['total_sales'] - cur_branch.get_sales_on_date(None, yesterdate, "monthly", None)
    metrics['abs_total_sales'] = abs(metrics['comp_total_sales'])
    print(sales_per_branch)
    return render(request, 'octo_site/dashboards/own_dashboard.html',
                  {'games': games, 'metrics': metrics, 'clues': clues,
                   'sales_per_branch': sales_per_branch,
                   'room_retentions': room_retentions,
                   'branch': cur_branch, 'cur_date': cur_date_str})
