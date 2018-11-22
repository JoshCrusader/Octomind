import paho.mqtt.client as mqtt  # import the client1
import time


############
def on_message(client, userdata, message):
    print("message received=", str(message.payload.decode("utf-8")))
    pass


broker_address = "localhost"
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback

client.connect(broker_address)  # connect to broke
while True:
    print("HI")
    time.sleep(3)  # wait
