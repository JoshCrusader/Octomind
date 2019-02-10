import paho.mqtt.client as mqtt  # import the client1
import time
import datetime
############
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8")).split(",")
    ts = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("message received=", str(message.payload.decode("utf-8")))
    file = open("testfile.txt","a") 

    file.write("abc\n") 
    file.close() 
    print("real time", ts)


broker_address = "localhost"
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback
client.connect(broker_address)  # connect to broke
client.subscribe("ccm/rpi_1")
print("client connected")

client.loop_forever()  # start the loop
            # client.loop_stop() #stop the loop
time.sleep(3)  # wait
