from ui import UI

import paho.mqtt.client as mqtt
import json
from config.mqtt import MQTTTopics as Topics
from config.mqtt import MQTTConfig 



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
    MQTTConfig.BROKER,
    MQTTConfig.PORT
)

#Połączenie backendu z UI UI otrzymuje dane w balloon/processed
client.subscribe(
    Topics.PROCESSED
)
client.loop_start()

print("UI started")

ui_module = UI()

ui_module.initialize_ui()
