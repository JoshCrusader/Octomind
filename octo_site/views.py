from django.shortcuts import render,redirect
from octo_site.models import *
# Create your views here.

def index(request):
    u = Users.objects.all()
    i = Info.objects.all()

    return render(request,'octo_site/index.html', {'u': u,'i': i,'ctr':0})
