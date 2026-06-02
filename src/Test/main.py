import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)

    print("Odebrano:", data)

    processed = {
        "strength": data["rssi"] * 2
    }

    print("Processed:", processed)

client = mqtt.Client()
client.on_message = on_message

client.connect("mqtt", 1883)
client.subscribe("balloon/raw")

client.loop_forever()