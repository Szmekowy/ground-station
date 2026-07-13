import json
import os
import paho.mqtt.client as mqtt


MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC_RAW = "balloon/raw"
MQTT_TOPIC_PROCESSED = "balloon/processed"

RAW_DATA_FILE = "data/raw/telemetry.jsonl"
PROCESSED_DATA_FILE = "data/processed/telemetry.jsonl"

def save_data(data, PATH): #zapis surowych danych do pliku
    print(PATH)
    os.makedirs(
        os.path.dirname(PATH),
        exist_ok=True
    )

    with open(PATH, "a") as file:
        file.write(
            json.dumps(data) + "\n"
        )


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

    save_data(data, PATH=RAW_DATA_FILE) #zapis surowych danych do plików (dla testów)


    processed = process_data(data)

    save_data(processed, PATH=PROCESSED_DATA_FILE) #zapis danych przetworzonych do pliku (dla testów)

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