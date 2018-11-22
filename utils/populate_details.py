from octo_site.models import *
import random
import math
import datetime
from datetime import timedelta

def gen_random(x):
    return math.ceil(random.random() * x)

def gen_r_random(x, y):
    return x + math.ceil(random.random() * (y - x))

def main_start():
    games = Game.objects.filter(room_id = 2)
    for game in games:
        detail = game.game_details
        dts = detail.timestart
        rd = gen_random(100)
        if(rd <= 60):
            detail.solved = 1
            r2 = gen_random(100)
            te = 60
            if(r2 <= 5):
                te = gen_r_random(20, 35)
            elif r2 <= 20:
                te = gen_r_random(35, 45)
            else:
                te = gen_r_random(45, 60)

            delta_time = timedelta(minutes = te, seconds = gen_r_random(0, 60))
            timee = dts + delta_time


            pass
        else:
            # Lose
            pass
    pass