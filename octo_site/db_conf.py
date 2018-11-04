import MySQLdb
from octo_site.models import *
import math
from datetime import datetime,timedelta
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
host = "localhost"


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

def pull_game_tally(game_id):
    data_return = []
    data = pull_data_fr_game(game_id)
    game = Game.objects.get(game_id=game_id)
    sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
    for s in sensors:
        data_return.append({
            "sensor_id": s.sensor_id,
            "sensor_name": s.sensor_name,
            "times_triggered": 0,
            "times_down": 0})
    for d in data:
        for dr in data_return:
            if dr["sensor_id"] == d["sensor_id"]:
                print(d["log_id"],d["sensor_id"],d["value"])
                if d["value"] == '1':
                    dr["times_triggered"] += 1
                else:
                    dr["times_down"] += 1

    return data_return

def pull_game_summary(game_id):
    '''
    *Match Overview*
    Skill Bracket: Normal Skill(finished 31-45mins), High Skill(finished less than 30/mins), Low Skill(46-60mins)
    Type: Walk-in/Scheduled
    Game: Alien/Rebeca/Aztec Assault
    Branch: CCM/31/Jupiter
    Duration:
    Match Ended: 24 minutes ago.
    '''

    game = Game.objects.get(game_id=game_id)
    f = '%Y-%m-%d %H:%M:%S'
    data_tally = pull_game_tally(game_id)
    data_sum_game = pull_data_game(game_id)
    time_finished = None
    skill_bracket = None
    average_times_bet_sensors = None
    ctr_avg = 0
    avg_sum = 0.0

    for data_sum in data_sum_game:
        if data_sum["time_solved"] != 0:
            avg_sum += float(data_sum["time_solved"])
            ctr_avg += 1

    data_return = {"sensor_info": None, "general_info": None}
    clean_date = datetime.strptime(game.game_details.timestart.strftime(f), f)
    try:
        datetime_object = datetime.strptime(game.game_details.timeend.strftime(f), f)
        time_diff = datetime_object - clean_date
        time_diff_in_min = time_diff / timedelta(minutes=1)
        time_finished = time_diff_in_min
    except:
        time_finished = clean_date + timedelta(minutes=math.floor(avg_sum),seconds=(avg_sum % 1))
        time_diff = time_finished - clean_date
        time_finished = round(time_diff / timedelta(minutes=1), 2)


    average_times_bet_sensors = round((float(avg_sum) / float(ctr_avg)), 2)

    if time_finished >= 31 and time_finished <= 45:
        skill_bracket = "Normal"
    elif time_finished >= 46 and time_finished <= 60:
        skill_bracket = "Low"
    elif time_finished <= 30:
        skill_bracket = "High"
    data_return["sensor_info"] = data_tally
    data_return["general_info"] = {
        "time_finished_duration": time_finished,
        "average_time": average_times_bet_sensors,
        "skill_bracket": skill_bracket
    }
    return data_return

## to write as summary function
def pull_data_game(game_id):
    #to_put_time_constraint here
    connection = MySQLdb.connect(host=host,user="root",passwd="root", db="sensorDB")
    cursor = connection.cursor()
    f = '%Y-%m-%d %H:%M:%S'
    prev_stamp=None
    time_diff_in_min = None
    new_data=[]
    game = Game.objects.get(game_id=game_id)
    sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
    sensors_id = []
    sensors_id_included = []
    for s in sensors:
        sensors_id.append(s.sensor_id)
    str_sensor_ids = "("+str(sensors_id).strip('[]')+")"

    data_return = []
    print(str_sensor_ids)
    # execute the SQL query using execute() method.
    cursor.execute("select * from sensor_log where sensor_id in "+str_sensor_ids+" and "+" timestamp between '"+game.game_details.timestart.strftime(f)+"' and DATE_ADD('"+game.game_details.timestart.strftime(f)+"', INTERVAL 1 HOUR);")

    # fetch all of the rows from the query
    data = cursor.fetchall()

    # print the rows
    for row in data:
        data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
    # close the cursor object
    # for summary data
    for s in sensors:
        for data in data_return:
            if s.sensor_id == data['sensor_id']:
                if s.sensor_type.trigger_treshold <= data['value']:
                    print(s.sensor_name+" triggered "+str(s.sensor_id)+"| log_id: "+str(data['log_id']))
                    if s.sequence_number == 1:
                        datetime_object = data['timestamp']
                        clean_date =datetime.strptime(game.game_details.timestart.strftime(f), f)
                        time_diff = datetime_object - clean_date
                        time_diff_in_min = time_diff / timedelta(minutes=1)
                        print(round(time_diff_in_min,1))
                        prev_stamp = data['timestamp']
                    else:
                        datetime_object = data['timestamp']
                        time_diff = datetime_object - prev_stamp
                        time_diff_in_min = time_diff / timedelta(minutes=1)
                        print(round(time_diff_in_min,1))
                        prev_stamp = data['timestamp']
                    new_data.append({"sensor_id": s.sensor_id, "time_solved": time_diff_in_min, "timestamp": data['timestamp']})
                    break
    for nd in new_data:
        sensors_id_included.append(nd['sensor_id'])

    for s in sensors:
        if s.sensor_id not in sensors_id_included:
            new_data.append({"sensor_id": s.sensor_id, "time_solved": 0, "timestamp": None})
    cursor.close()
    # close the connection
    connection.close()
    print(new_data)
    return new_data
def transmogrify_data(dataset_logs):
    for data in dataset_logs:
        sensor = Sensor.objects.get(sensor_id=data["sensor_id"])
        if int(data['value']) >= sensor.sensor_type.trigger_treshold:
            data['value'] = '1'
        else:
            data['value'] = '0'
    return dataset_logs
def pull_data_live_control_panel(game_id):
    game = Game.objects.get(game_id=game_id)
    check_seq(game)

    return pull_data_fr_game(game_id)
def pull_data_fr_game(game_id):
    connection = MySQLdb.connect(host=host,user="root",passwd="root", db="sensorDB")
    cursor = connection.cursor()
    f = '%Y-%m-%d %H:%M:%S'
    game = Game.objects.get(game_id=game_id)
    sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
    sensors_id = []
    for s in sensors:
        sensors_id.append(s.sensor_id)
    str_sensor_ids = "(" + str(sensors_id).strip('[]') + ")"

    data_return = []
    # execute the SQL query using execute() method.
    cursor.execute("select * from sensor_log where sensor_id in "+str_sensor_ids+" and "+" timestamp between '"+game.game_details.timestart.strftime(f)+"' and DATE_ADD('"+game.game_details.timestart.strftime(f)+"', INTERVAL 1 HOUR);")

    # fetch all of the rows from the query
    data = cursor.fetchall()
    # print the rows
    for row in data:
        data_return.append({"log_id": row[0], "timestamp": row[1], "sensor_id": row[2], "value": row[3]})
        # close the cursor object

    cursor.close()
    # close the connection
    connection.close()
    return transmogrify_data(data_return)
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

def check_seq(game):
    in_seq = True
    sensors = Room.objects.get(room_id=game.room.room_id).get_all_sensors
    seq = []
    cur_seq = []
    log_data = pull_data_fr_game(game.game_id)
    trigger_seqs = {}
    for s in sensors:
        trigger_seqs[str(s.sensor_id)] = None
        seq.append(s.sensor_id)
    trigger_seq =1
    skip_sensors =[]
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
                print(str(s.sensor_name)+" not in sequence")
                in_seq = False
    if in_seq:
        print("all is insequence so far")
    else:
        print("wew")
    return in_seq


