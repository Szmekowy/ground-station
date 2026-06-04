import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client()
client.connect("mqtt", 1883)

def get_data():
    return {"rssi": -70, "signal": "raw", "time": time.time()}

while True:
    data = get_data()

    client.publish(
        "balloon/raw",
        json.dumps(data)
    )

    time.sleep(1)