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
        z = gen_r_random(1, 3)
        for i in range(0, z):
            cd = ClueDetails(detail = 'No Detail avail', timestamp = dts+timedelta(minutes = gen_r_random(6, te-2), seconds = gen_r_random(0, 58)) )
            cd.save()
            clue = Clues(clue_details_id = cd.clue_details_id, game_id = game.game_id)
            clue.save()


def gen_error(chance, dts, si, game):
    if (gen_random(100) <= chance):
        z = gen_r_random(1, 3)
        for i in range(0, z):
            cd = ClueDetails(detail='No Detail avail',
                             timestamp=dts + timedelta(minutes=gen_r_random(6, te - 2), seconds=gen_r_random(0, 58)))
            cd.save()
            clue = Clues(clue_details_id=cd.clue_details_id, game_id=game.game_id)
            clue.save()


def main_start():
    games = Game.objects.filter(game_id__gte=939)
    for game in games:
        
        rd = gen_random(100)
        if(rd <= 55):
            detail = GameDetails.objects.get(game_details_id = game.game_details_id)
            dts = detail.timestart
            detail.solved = 1
            r2 = gen_random(100)
            te = 60
            if(r2 <= 5):
                te = gen_r_random(10, 35)
                gen_clues(5, dts, te, game)
            elif r2 <= 20:
                te = gen_r_random(35, 45)
                gen_clues(5, dts, te, game)
            else:
                te = gen_r_random(45, 58)
                gen_clues(40, dts, te, game)

            delta_time = timedelta(minutes = te, seconds = gen_r_random(0, 58))
            timee = dts + delta_time
            
            detail.timeend = timee
            detail.save()
        else:
            detail = game.game_details
            dts = detail.timestart
            t3 = gen_random(100)
            te = 60
            detail.solved = 0
            delta_time = timedelta(minutes = te)
            if(t3 <= 14):
                te = gen_r_random(15, 50)
                gen_clues(58, dts, te, game)
                delta_time = timedelta(minutes = te, seconds = gen_r_random(0, 58))
                timee = dts + delta_time
                detail.timeend = timee
                detail.save()
            else:
                print('d natapos')
                detail.timeend = None
                detail.save()
                gen_clues(40, dts, te, game)
            
    print('done')


def sec_start():
    games = Game.objects.filter(room_id=2).filter(game_id__gte=939)
    for game in games:
        detail = game.game_details
        dts = detail.timestart
        rd = gen_random(100)
        if (rd <= 12):
            detail.solved = 1
            r2 = gen_random(100)
            te = 60
            if (r2 <= 5):
                te = gen_r_random(20, 35)
                gen_clues(5, dts, te, game)
            elif r2 <= 20:
                te = gen_r_random(35, 45)
                gen_clues(5, dts, te, game)
            else:
                te = gen_r_random(45, 58)
                gen_clues(40, dts, te, game)

            delta_time = timedelta(minutes=te, seconds=gen_r_random(0, 58))
            timee = dts + delta_time

            detail.timeend = timee
            detail.save()
        else:
            t3 = gen_random(100)
            te = 60

            delta_time = timedelta(minutes=te)
            if (t3 <= 7):
                te = gen_r_random(15, 50)
                gen_clues(58, dts, te, game)
                delta_time = timedelta(minutes=te, seconds=gen_r_random(0, 58))
                timee = dts + delta_time
                detail.timeend = timee
                detail.save()
            else:
                gen_clues(40, dts, te, game)

    print('done')