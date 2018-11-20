from django.shortcuts import render
from octo_site.models import *
from django.http import HttpResponseRedirect, JsonResponse
from octo_site.reports_controller import *

def market_analysis(request):
    return render(request, 'octo_site/reports/market/market_analysis.html')