from octo_site.models import *
import random
import math
import datetime
from datetime import timedelta

def gen_random(x):
    return math.ceil(random.random() * x)

def gen_r_random(x, y):
    return x + math.ceil(random.random() * (y - x))

def gen_clues(chance, dts, te, game):
    if(gen_random(100) <= chance):
        z = 3
        if(gen_random(100) <= 30):
            z = gen_r_random(1, 2)
        for i in range(0, z):
            crandd = gen_random(100)
            ce = gen_r_random(6, min(te-2, 25))
            if(crandd <= 40):
                ce = gen_r_random(6, te-2)
            cd = ClueDetails(detail = 'No Detail avail', timestamp = dts+timedelta(minutes = ce, seconds = gen_r_random(0, 58)) )
            cd.save()
            clue = Clues(clue_details_id = cd.clue_details_id, game_id = game.game_id)
            clue.save()
def main_start():
    games = Game.objects.filter(room_id = 3)
    for game in games:
        detail = game.game_details
        dts = detail.timestart
        rd = gen_random(100)
        if(rd <= 35):
            detail.solved = 1
            r2 = gen_random(100)
            te = 60
            if(r2 <= 0):
                te = gen_r_random(20, 35)
                gen_clues(5, dts, te, game)
            elif r2 <= 0:
                te = gen_r_random(35, 45)
                gen_clues(5, dts, te, game)
            else:
                te = gen_r_random(45, 58)
                gen_clues(73, dts, te, game)

            delta_time = timedelta(minutes = te, seconds = gen_r_random(0, 58))
            timee = dts + delta_time
            
            detail.timeend = timee
            detail.save()
        else:
            t3 = gen_random(100)
            te = 60
            detail.solved = 0
            delta_time = timedelta(minutes = te)
            if(t3 <= 14):
                randn = gen_random(100)
                te = gen_r_random(15, 50)
                if(randn <= 60):
                    te = gen_r_random(15, 28)
                gen_clues(90, dts, te, game)
                delta_time = timedelta(minutes = te, seconds = gen_r_random(0, 58))
                timee = dts + delta_time
                detail.timeend = timee
                detail.save()
            else:
                
                detail.timeend = None
                detail.save()
                gen_clues(70, dts, te, game)
            
    print('done')