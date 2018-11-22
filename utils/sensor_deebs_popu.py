from octo_site.models import *
import random
import math
import datetime
from datetime import timedelta

import MySQLdb

def insert_val(sid,ts,val):
    ts = str(ts.strftime("%Y-%m-%d %H:%M:%S"))
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="sensorDB")
    x = conn.cursor()
    try:
        x.execute("INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);", (sid, ts, val))
        conn.commit()
        print("inserted!")
    except Exception as e:
        print(e)
        conn.rollback()

    conn.close()

    conn.close()
def gen_random(x):
    return math.ceil(random.random() * x)


def gen_r_random(x, y):
    return x + math.ceil(random.random() * (y - x))


def gen_clues(dts, te, game):
    if (gen_random(100) <= chance):
        z = gen_r_random(1, 3)
        for i in range(0, z):
            cd = ClueDetails(detail='No Detail avail',
                             timestamp=dts + timedelta(minutes=gen_r_random(6, te - 2), seconds=gen_r_random(0, 58)))
            cd.save()
            clue = Clues(clue_details_id=cd.clue_details_id, game_id=game.game_id)
            clue.save()


def gen_log_db(case, dts , game):
    sensors = game.room.get_all_sensors
    cum_solve_time = 0
    if case == 1:
        for s in sensors:
            min_solve = gen_r_random(6,15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)
    if case == 2:
        for s in sensors:
            min_solve = gen_r_random(6,15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time

            insert_val(s.sensor_id, ts, 1)

            if gen_random(100) <= 60:
                delta_time = timedelta(minutes=cum_solve_time+gen_r_random(0, 9), seconds=gen_r_random(0, 58))
                ts = dts + delta_time
                insert_val(s.sensor_id, ts, 0)

def main_start():
    games = Game.objects.filter(room_id=2)
    for game in games:
        detail = game.game_details
        sensors = game.room.get_all_sensors
        dts = detail.timestart
        rd = gen_random(100)
        if (rd <= 60):
            if(detail.solved ==1):
                for s in sensors:
                    insert_val(s.sensor_id,dts,0)

                r2 = gen_random(100)
                if 0 > r2 <= 5:     #case 3
                    pass
                elif 5 > r2 <= 65:  #case1
                    te = gen_r_random(35, 45)
                    gen_clues(1, dts, game)
                elif 65 > r2 <= 95: #case2
                    te = gen_r_random(35, 45)
                    gen_clues(2, dts, game)
                else:               #case4
                    pass
    print('done')
def dupe():
    games = Game.objects.filter(room_id=2)
    for game in games:
        detail = game.game_details
        dts = detail.timestart
        rd = gen_random(100)
        if (rd <= 60):
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

def sec_start():
    games = Game.objects.filter(room_id=2)
    for game in games:
        detail = game.game_details
        dts = detail.timestart
        rd = gen_random(100)
        if (rd <= 12):
            r2 = gen_r_random(1, 4)
            if r2 == 1:
                te = gen_r_random(0, 15)
                gen_error(12, dts, te, game)
            elif r2 == 2:
                te = gen_r_random(16, 30)
                gen_error(5, dts, te, game)
            elif r2 == 3:
                te = gen_r_random(31, 45)
                gen_error(5, dts, te, game)
            else:
                te = gen_r_random(46, 59)
                gen_error(40, dts, te, game)

            '''
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
            '''
        else:
            pass

    print('done')
