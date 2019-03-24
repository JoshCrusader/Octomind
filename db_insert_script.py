import paho.mqtt.client as mqtt  # import the client1
import time
import MySQLdb
import datetime
# alien assault sensors: 26,27,28,29
def store(a, b):
    ts = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="sensorDB")
    x = conn.cursor()
    try:
        x.execute("INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);", (a, ts,b))
        conn.commit()
        print("inserted!")
    except Exception as e:
        print (e)
        print("wats")
        conn.rollback()
    conn.close()
    pass

while True:
    a = input("sensor_id: ")
    b = input("value: ")
    store(a,b)
