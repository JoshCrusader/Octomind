from octo_site.models import *
import random
import math
import datetime
from datetime import timedelta

def genrand():
    return math.floor(random.random()*100)

def gennum(x, y):
    return math.floor(random.random()*x)+y
def gen_random(x):
    return math.ceil(random.random() * x)

def gen_r_random(x, y):
    return x + math.ceil(random.random() * (y - x))

def gen_day():
    rng = genrand()
    if(rng <= 40):
        return gen_r_random(0,10)
    elif(rng <= 80):
        return gen_r_random(28,30)
    else:
        return gen_r_random(11, 27)

def get_m(x):
    if("Apr" in x):
        return 4
    elif("Myy" in x):
        return 5
    elif("Jun" in x):
        return 6
    elif("Jul" in x):
        return 7
    elif("Aug" in x):
        return 8
    elif("Sep" in x):
        return 9
    elif("Oct" in x):
        return 10
    elif("Nov" in x):
        return 11
    else:
        return 12
def popu_start():
    gems = GameDetails.objects.all()
    for gem in gems:
        if(gem.timestart is None):

            # day = gen_day()
            day = gen_r_random(1,30)
            mon = get_m(gem.teamname)
            det = datetime.datetime(2019, mon, day)
            delta_time = det+timedelta(hours = 12, minutes = 0, seconds = 0)
            gem.timestart = delta_time
            gem.save()
    pass