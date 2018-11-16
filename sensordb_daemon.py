import paho.mqtt.client as mqtt  # import the client1
import time
import MySQLdb
############
def on_message(client, userdata, message):
    print("message received=", str(message.payload.decode("utf-8")))
    msg = str(message.payload.decode("utf-8")).split(",")
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="sensorDB")
    x = conn.cursor()

    try:
        x.execute("INSERT INTO `sensorDB`.`sensor_log` (`log_id`,`sensor_id`, `timestamp`, `value`) VALUES (null, %s, %s, %s);", (msg[0], msg[1], msg[2]))
        conn.commit()
        print("inserted!")
    except:
        conn.rollback()

    conn.close()
    pass

broker_address = "localhost"
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback

client.connect(broker_address)  # connect to broke
while True:
    client.subscribe("ccm/rpi_1")
    client.loop_start()  # start the loop
    # client.loop_stop() #stop the loop
    time.sleep(3)  # wait
