from polly import Polly
import paho.mqtt.client as mqtt
import sys


print("Starting MQTTS")
sys.stdout.flush()
polly_tts = Polly('Brian')

def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print("ONCONNECT")
    client.subscribe("jarvis/tts")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "jarvis/tts":
        txt = msg.payload.decode("utf-8")
        print("TTS: "+txt)
        sys.stdout.flush()
        fname = polly_tts.processText(txt)
        print(fname)
        sys.stdout.flush()
        polly_tts.cleanup()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("pizero1", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
