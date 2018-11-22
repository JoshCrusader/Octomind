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
    except Exception as e:
        print(e)
        conn.rollback()
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

def gen_error(ts,det,game,si,sensor_seq):
    app =[]
    for s in sensor_seq:
        app.append(s.sensor_id)
    er = GameErrorLog(game_id=game.game_id,timestamp=ts,details=det,sensor_id=si,cur_sensor_seq=app)
    er.save()

def gen_warning(ts, det, game, si,time_solved):
    wa = GameWarningLog(game_id=game.game_id, timestamp=ts, details=det, sensor_id=si, time_solved=time_solved)
    wa.save()

def gen_log_db(case, dts , game):
    sensors = game.room.get_all_sensors
    case_3_sensors = []
    case_3_sensors.append(sensors[1])
    case_3_sensors.append(sensors[0])
    case_3_sensors.append(sensors[2])
    case_3_sensors.append(sensors[3])
    cum_solve_time = 0

    if case == 1:
        for s in sensors:
            print("case!",case)
            min_solve = gen_r_random(4,15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)
    elif case == 2:
        for s in sensors:
            print("case!",case)
            min_solve = gen_r_random(8,16)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)

            if gen_random(100) <= 50:
                delta_time = timedelta(minutes=gen_r_random(0, 9), seconds=gen_r_random(0, 58))
                ts = ts + delta_time
                insert_val(s.sensor_id, ts, 0)
            else:
                delta_time = timedelta(minutes=gen_r_random(0, 2), seconds=gen_r_random(0, 58))
                ts = dts + delta_time
                insert_val(s.sensor_id, ts, 0)
                delta_time = timedelta(minutes=gen_r_random(1, 3), seconds=gen_r_random(0, 58))
                ts = ts + delta_time
                insert_val(s.sensor_id, ts, 1)
    elif case == 3:
        if gen_random(100) <= 70:
            for s in case_3_sensors:
                min_solve = gen_r_random(8, 16)
                cum_solve_time += min_solve
                delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                ts = dts + delta_time
                insert_val(s.sensor_id, ts, 1)
                gen_error(ts,"Sensor "+s.sensor_name+" not in sequence",game,s.sensor_id,case_3_sensors)
                print("case!",case)
                if gen_random(100) <= 50:
                    delta_time = timedelta(minutes=gen_r_random(0, 9), seconds=gen_r_random(0, 58))
                    ts = ts + delta_time
                    insert_val(s.sensor_id, ts, 0)
                else:
                    delta_time = timedelta(minutes=gen_r_random(0, 2), seconds=gen_r_random(0, 58))
                    ts = dts + delta_time
                    insert_val(s.sensor_id, ts, 0)
                    delta_time = timedelta(minutes=gen_r_random(1, 3), seconds=gen_r_random(0, 58))
                    ts = ts + delta_time
                    insert_val(s.sensor_id, ts, 1)
        else:
            for s in sensors:
                print("case!", case)
                min_solve = gen_r_random(8, 15)
                if gen_random(100) <= 70:
                    min_solve = gen_r_random(3, 5)
                    cum_solve_time += min_solve
                    delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                    ts = dts + delta_time
                    insert_val(s.sensor_id, ts, 1)
                    gen_warning(ts,"Sensor "+s.sensor_name+" solved too fast",game,s.sensor_id,min_solve)
                else:
                    cum_solve_time += min_solve
                    delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                    ts = dts + delta_time
                    insert_val(s.sensor_id, ts, 1)
def gen_log_lose(case, dts , game):
    sensors = game.room.get_all_sensors
    case_3_sensors = []
    case_3_sensors.append(sensors[1])
    case_3_sensors.append(sensors[0])
    case_3_sensors.append(sensors[2])
    case_3_sensors.append(sensors[3])
    cum_solve_time = 0

    if case == 1:
        ss =sensors[:-1]
        cs = case_3_sensors[:-1]
        if gen_random(100) <= 50:
            ss = sensors[:-2]
            cs = case_3_sensors[:-2]
        if gen_random(100) <= 70:
            for s in ss:
                print("case!",case)
                min_solve = gen_r_random(4,15)
                cum_solve_time += min_solve
                delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                ts = dts + delta_time
                insert_val(s.sensor_id, ts, 1)
        else:
            for s in case_3_sensors:
                min_solve = gen_r_random(8, 16)
                cum_solve_time += min_solve
                delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                ts = dts + delta_time
                insert_val(s.sensor_id, ts, 1)
                gen_error(ts,"Sensor "+s.sensor_name+" not in sequence",game,s.sensor_id,case_3_sensors)
                print("case!",case)
                if gen_random(100) <= 50:
                    delta_time = timedelta(minutes=gen_r_random(0, 9), seconds=gen_r_random(0, 58))
                    ts = ts + delta_time
                    insert_val(s.sensor_id, ts, 0)
                else:
                    delta_time = timedelta(minutes=gen_r_random(0, 2), seconds=gen_r_random(0, 58))
                    ts = dts + delta_time
                    insert_val(s.sensor_id, ts, 0)
                    delta_time = timedelta(minutes=gen_r_random(1, 3), seconds=gen_r_random(0, 58))
                    ts = ts + delta_time
                    insert_val(s.sensor_id, ts, 1)
    elif case == 2:
        if gen_random(100) <= 80:
            s=sensors[0]
        else:
            s = sensors[1]
        print("case!",case)
        min_solve = gen_r_random(8,16)
        cum_solve_time += min_solve
        delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
        ts = dts + delta_time
        insert_val(s.sensor_id, ts, 1)

        if gen_random(100) <= 50:
            delta_time = timedelta(minutes=gen_r_random(0, 9), seconds=gen_r_random(0, 58))
            ts = ts + delta_time
            insert_val(s.sensor_id, ts, 0)
        else:
            delta_time = timedelta(minutes=gen_r_random(0, 2), seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 0)
            delta_time = timedelta(minutes=gen_r_random(1, 3), seconds=gen_r_random(0, 58))
            ts = ts + delta_time
            insert_val(s.sensor_id, ts, 1)

def main_start():
    print("zuc starting")
    games = Game.objects.filter(room_id=2)
    for game in games:
        detail = game.game_details
        sensors = game.room.get_all_sensors
        dts = detail.timestart

        for s in sensors:
            insert_val(s.sensor_id, dts, 0)
        if(detail.solved ==1):
            r2 = gen_r_random(1,100)
            if r2 > 0 and r2 <= 65:     #case 1
                gen_log_db(1, dts, game)
            elif r2 > 66 and r2 <= 92:  #case2
                gen_log_db(2, dts, game)
            else:
                gen_log_db(3, dts,game)
                #cases 3 & 4
                pass
        else:
            if game.get_game_conclusion == "forfeit":
                #upto sensor 1 or 2 only
                r2 = gen_r_random(1, 100)
                if r2 > 0 and r2 <= 70:  # case 1
                    gen_log_lose(4, dts, game)
                else:
                    gen_log_lose(5, dts, game)
                    # cases 3 & 4
                    pass
            else:
                r2 = gen_r_random(1, 100)
                if r2 > 0 and r2 <= 85:  # case 1
                    gen_log_lose(1, dts, game)
                elif r2 > 85 and r2 <= 98:  # case2
                    gen_log_lose(2, dts, game)
                else:
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
