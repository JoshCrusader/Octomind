from django.shortcuts import render
from octo_site.models import *
import json

def market_report(request):
    return render(request,'octo_site/reports/market_report.html')