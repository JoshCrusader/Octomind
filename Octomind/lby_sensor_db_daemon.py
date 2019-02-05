import paho.mqtt.client as mqtt  # import the client1
import time
import MySQLdb
import datetime
############
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")).split(",")
    ts = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    msg=str(message.payload.decode("utf-8"))
    msgs = msg.split(",")
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="sensorDB")
    x = conn.cursor()
    try:
        x.execute("INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);", (msgs[0], ts, msgs[2]))
        conn.commit()
        print("inserted!",msgs)
    except Exception as e:
        print (e)
        print("wats")
        conn.rollback()

    conn.close()
    pass

broker_address = "192.168.43.225"
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback
client.connect(broker_address)  # connect to broke
print("client connected")
while True:
    client.subscribe("ccm/rpi_1")
    client.loop_start()  # start the loop
    # client.loop_stop() #stop the loop
    time.sleep(3)  # wait
