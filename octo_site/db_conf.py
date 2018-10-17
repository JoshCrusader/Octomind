import MySQLdb
from octo_site.models import *

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
def pull_data():
    data_return = []
    host = "localhost"
    connection = MySQLdb.connect(
        host=host,
        user="root",
        passwd="root",
        db="sensorDB")

    # prepare a cursor object using cursor() method
    cursor = connection.cursor()

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
    #to_put_time_constraint here
    rpi_ids = []
    rpis = Rpi.objects.filter(room_id=room_id)
    for rpi in rpis:
        rpi_ids.append(rpi.rpi_id)

    data_return = []
    host = "localhost"
    connection = MySQLdb.connect(
        host=host,
        user="root",
        passwd="root",
        db="sensorDB")

    # prepare a cursor object using cursor() method
    cursor = connection.cursor()

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

def manual_query(query):

    data_return = []
    host = "localhost"
    connection = MySQLdb.connect(
        host=host,
        user="root",
        passwd="root",
        db="sensorDB")

    # prepare a cursor object using cursor() method
    cursor = connection.cursor()
    # execute the SQL query using execute() method.
    cursor.execute("select * from sensor_log")
   # sql = "INSERT INTO `sensorDB`.`sensor_log` ( `timestamp`,`sensor_id`,`value`) VALUES (%s, %s, %s);"
    cursor.execute(query)
    # fetch all of the rows from the query
    data = cursor.fetchall()
    cursor.close()
    # close the connection
    connection.close()
    return data
