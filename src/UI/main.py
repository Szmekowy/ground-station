from ui import UI

import paho.mqtt.client as mqtt
import json


MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "balloon/processed"

def on_message(client, userdata, msg):

    data = json.loads(
        msg.payload.decode()
    )

    update_ui(data)

def update_ui(data):
    time = data['timestamp']
    battery = data['battery']
    alt = data['altitude']
    pressure = data['pressure']
    ui_module.update_battery(battery)
    ui_module.update_altitude({'time': time, 'altitude': alt})
    ui_module.update_pressure({'time': time, 'pressure': pressure})

client = mqtt.Client()

client.on_message = on_message


client.connect( #połączenie z MQTT
    MQTT_BROKER,
    MQTT_PORT
)

#Połączenie backendu z UI UI otrzymuje dane w balloon/processed
client.subscribe(
    MQTT_TOPIC
)
client.loop_start()

print("UI started")

ui_module = UI()

ui_module.initialize_ui()
