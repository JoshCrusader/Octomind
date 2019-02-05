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
    print("message received--")
    print("sensor ID: ",msgs[0])
    print("timestamped: ",msgs[1])
    print("value recorded: ",msgs[2])
    file = open("testfile.txt","a") 

    file.write(msg+"\n") 
     
    file.close() 
    pass

broker_address = "localhost"
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback
client.connect(broker_address)  # connect to broke
print("client connected")
while True:
    client.subscribe("ccm/rpi_1")
    client.loop_start()  # start the loop
    # client.loop_stop() #stop the loop
    time.sleep(3)  # wait
