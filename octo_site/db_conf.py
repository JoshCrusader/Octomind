import MySQLdb
from octo_site.models import *
import math
from datetime import datetime,timedelta
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
host = "localhost"



## fixing
def pull_game_tally(game_id):
    g = Game.objects.get(game_id=game_id)
    return g.pull_game_tally(g)
def pull_game_summary(game_id):
    return Game.objects.get(game_id=game_id).pull_game_summary
## to write as summary function
def pull_data_game(game_id):
    return Game.objects.get(game_id=game_id).pull_data_game
def pull_data_live_control_panel(game_id):
    g = Game.objects.get(game_id=game_id)
    check_seq(g)
    return g.pull_data_fr_game(g)

def check_seq(game):
#<<<<<<< HEAD
    # print("checking_seq")
    if game.has_error:
        error_sensor = game.get_error_points_sensors
        print("has error")
        for s in error_sensor:
            print(s.sensor_name, "not in sequence")
#=======
    in_seq = True
    sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
    seq = []
    log_data = game.pull_data_fr_game(game)
    trigger_seqs = {}
    for s in sensors:
        trigger_seqs[str(s.sensor_id)] = None
        seq.append(s.sensor_id)
    trigger_seq = 1
    skip_sensors = []
#>>>>>>> 5b3cc82ec138458a2a3ae2613437955936dd8487

    for data in log_data:
        s = Sensor.objects.get(sensor_id=data['sensor_id'])
        if 1 == int(data['value']) and s.sensor_id not in skip_sensors:

            skip_sensors.append(s.sensor_id)
            trigger_seqs[str(s.sensor_id)] = trigger_seq
            trigger_seq += 1

    print(trigger_seqs)
    for t in trigger_seqs:
        if trigger_seqs[t] is not None:
            s = Sensor.objects.get(sensor_id=t)
            if s.sequence_number != trigger_seqs[t]:
                if GameErrorLog.error_not_log_existing(game.game_id, s.sensor_id):
                    game_error_log = GameErrorLog(
                        game_id=game.game_id,
                        sensor_id=s.sensor_id,
                        details=str(s.sensor_name) + " not in sequence",
                        timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                        cur_sensor_seq=game.get_sensor_trigger_sequence
                    )
                    game_error_log.save()
                    print("error inserted")
                print(str(s.sensor_name) + " not in sequence")
                in_seq = False
    if in_seq:
        print("all is insequence so far")
    return in_seq
# UNUSED FUNCTIONS
def pull_data():
    connection = MySQLdb.connect(
        host=host,
        user="root",
        passwd="root",
        db="sensorDB")
    cursor = connection.cursor()
    data_return = []
    # prepare a cursor object using cursor() method
    # execute the SQL query using execute() method.
    cursor.execute("select * from sensor_log")
    # fetch all of the rows from the query
    data = cursor.fetchall()

    # print the rows
    for row in data:
        data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
    # close the cursor object
    cursor.close()
    # close the connection
    connection.close()

    return data_return
def pull_data_room(room_id):
    connection = MySQLdb.connect(host=host,user="root",passwd="root", db="sensorDB")
    cursor = connection.cursor()
    rpi_ids = []
    rpis = Rpi.objects.filter(room_id=room_id)
    for rpi in rpis:
        rpi_ids.append(rpi.rpi_id)

    data_return = []

    # execute the SQL query using execute() method.
    cursor.execute("select * from sensor_log")

    # fetch all of the rows from the query
    data = cursor.fetchall()

    # print the rows
    for row in data:
        if Sensor.objects.get(sensor_id=row[2]).rpi_id in rpi_ids:
            data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
    # close the cursor object
    cursor.close()
    # close the connection
    connection.close()
    return data_return

