from django.shortcuts import render
from octo_site.models import *
from django.http import HttpResponseRedirect, JsonResponse
from octo_site.reports_controller import *

def player_analysis_report(request):
    return render(request, 'octo_site/reports/market/player_analysis_report/main.html')