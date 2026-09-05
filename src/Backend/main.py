import json
import os
import paho.mqtt.client as mqtt
from storage.JSON.json_storage import JsonStorage
from storage.JSON.json_read import JsonReader
from storage.database.database_storage import DatabaseStorage
from storage.database.connection import get_session
from config.mqtt import MQTTTopics as Topics
from config.mqtt import MQTTConfig 


session = get_session()

storage = DatabaseStorage(
    session
)
#storage = JsonStorage()
reader = JsonReader()

def process_data(data): #processing testowych danych

    processed = {
        "timestamp": data["timestamp"],
        "altitude": data["position"]["z"],
        "battery": data["battery"],
        "pressure": data["pressure"] * 2
    }

    return processed

def on_message(client, userdata, msg): #backend odpytuje MQTT czy są nowe dane jeżeli tak to przetwarza i zapisuje dane do plików


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
        Topics.PROCESSED,
        json_data
    )

    print("Published for UI:", json_data)

if __name__ == "__main__":

    client = mqtt.Client()

    client.on_message = on_message


    client.connect( #połączenie z MQTT
        MQTTConfig.BROKER,
        MQTTConfig.PORT
    )

    #Połączenie backendu z Communication backend otrzymuje dane w balloon/raw
    client.subscribe(
        Topics.RAW
    )


    print(
        f"Backend listening on {Topics.RAW}"
        
    )
    print(
        f"Backend sending on {Topics.PROCESSED}"
        
    )


    client.loop_forever()