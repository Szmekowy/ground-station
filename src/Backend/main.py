import json
import os
import paho.mqtt.client as mqtt
from storage.JSON.json_storage import JsonStorage


MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC_RAW = "balloon/raw"
MQTT_TOPIC_PROCESSED = "balloon/processed"


def process_data(data): #processing testowych danych

    processed = {
        "timestamp": data["timestamp"],
        "altitude": data["position"]["z"],
        "battery": data["battery"],
        "pressure": data["pressure"] * 2
    }

    return processed

def on_message(client, userdata, msg): #backend odpytuje MQTT czy są nowe dane jeżeli tak to przetwarza i zapisuje dane do plików

    storage = JsonStorage()

    data = json.loads(
        msg.payload.decode("utf-8")
    )

    storage.save_raw(data) #zapis surowych danych do plików (dla testów)


    processed = process_data(data)

    storage.save_processed(processed) #zapis danych przetworzonych do pliku (dla testów)

    publish_data(processed) #publikacja danych przetworzonych do UI

def publish_data(data):

    json_data = json.dumps(data)

    client.publish(
        MQTT_TOPIC_PROCESSED,
        json_data
    )

    print("Published for UI:", json_data)


if __name__ == "__main__":
    client = mqtt.Client()

    client.on_message = on_message


    client.connect( #połączenie z MQTT
        MQTT_BROKER,
        MQTT_PORT
    )

    #Połączenie backendu z Communication backend otrzymuje dane w balloon/raw
    client.subscribe(
        MQTT_TOPIC_RAW
    )


    print(
        f"Backend listening on {MQTT_TOPIC_RAW}"
        
    )
    print(
        f"Backend sending on {MQTT_TOPIC_PROCESSED}"
        
    )


    client.loop_forever()