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
    print("checking_seq")
    if game.has_error:
        error_sensor = game.get_error_points_sensors
        print("has error")
        for s in error_sensor:
            print(s.sensor_name, "not in sequence")

    return game.has_error
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

