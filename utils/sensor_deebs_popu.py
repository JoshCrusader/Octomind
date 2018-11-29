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



def gen_error(ts,det,game,si,sensor_seq):
    app=[]
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
    case_3_sensors.append(sensors[4])
    cum_solve_time = 0

    if case == 1:
        no_error_chance = gen_random(100)
        if no_error_chance <= 76:
            for s in sensors:
                print("case!",case)
                min_solve = gen_r_random(6,12)
                cum_solve_time += min_solve
                delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                ts = dts + delta_time
                insert_val(s.sensor_id, ts, 1)
        else:
            error_type_chance = gen_random(100)
            if error_type_chance <= 40:
                random_sensor = gen_r_random(2,4)
                for i,s in enumerate(sensors):
                    min_solve = gen_r_random(6, 12)
                    if i == random_sensor:
                        min_solve = gen_r_random(2, 4)
                    cum_solve_time += min_solve
                    delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                    ts = dts + delta_time
                    insert_val(s.sensor_id, ts, 1)
                    gen_warning(ts,"Sensor "+s.sensor_name+" solved questionably",game,s.sensor_id,min_solve)
            else:
                for s in case_3_sensors:
                    print("case!",case)
                    min_solve = gen_r_random(6,12)
                    cum_solve_time += min_solve
                    delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
                    ts = dts + delta_time
                    insert_val(s.sensor_id, ts, 1)
                    if s.sensor_id == case_3_sensors[1].sensor_id:
                        gen_error(ts, "Sensor " + s.sensor_name + " not in sequence", game, s.sensor_id, case_3_sensors)
                    elif s.sensor_id == case_3_sensors[0].sensor_id:
                        gen_error(ts, "Sensor " + s.sensor_name + " not in sequence", game, s.sensor_id, case_3_sensors)


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
        for s in ss:
            print("case!",case)
            min_solve = gen_r_random(4,15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)

    elif case == 2:
        ss = sensors[:-2]
        for s in ss:
            print("case!", case)
            min_solve = gen_r_random(4, 15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)
    elif case == 3:
        ss = sensors[:-3]
        for s in ss:
            print("case!", case)
            min_solve = gen_r_random(4, 15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)
    elif case == 4:
        ss = sensors[:-1]
        for s in ss:
            print("case!", case)
            min_solve = gen_r_random(4, 15)
            cum_solve_time += min_solve
            delta_time = timedelta(minutes=cum_solve_time, seconds=gen_r_random(0, 58))
            ts = dts + delta_time
            insert_val(s.sensor_id, ts, 1)

def main_start():
    print("zuc starting")
    games = Game.objects.filter(room_id=9)
    for game in games:
        detail = game.game_details
        sensors = game.room.get_all_sensors
        dts = detail.timestart
        if dts is not None:
            for s in sensors:
                insert_val(s.sensor_id, dts, 0)

            if(detail.solved == 1):
                    print("wonned")
                    gen_log_db(1, dts, game)
            else:
                print("losted")
                if game.get_game_conclusion == "forfeit":
                    #upto sensor 1 or 2 only
                    r2 = gen_r_random(1, 100)
                    if r2 > 0 and r2 <= 80:  # case 1
                        gen_log_lose(3, dts, game)
                    else:
                        gen_log_lose(4, dts, game)
                else:
                    r2 = gen_r_random(1, 100)
                    if r2 > 0 and r2 <= 50:  # case 1
                        gen_log_lose(1, dts, game)
                    else:  # case2
                        gen_log_lose(2, dts, game)

    print('done')