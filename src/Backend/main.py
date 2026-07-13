import json
import os
import paho.mqtt.client as mqtt


MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "balloon/raw"

RAW_DATA_FILE = "data/raw/telemetry.jsonl"
PROCESSED_DATA_FILE = "data/processed/telemetry.jsonl"

def save_data(data, PATH): #zapis surowych danych do pliku

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

    print("Received:")
    print(data)


    save_data(data, PATH=RAW_DATA_FILE)


    processed = process_data(data)

    print("Processed:")
    print(processed)

    save_data(processed, PATH=PROCESSED_DATA_FILE)

if __name__ == "__main__":
    client = mqtt.Client()

    client.on_message = on_message


    client.connect( #połączenie z MQTT
        MQTT_BROKER,
        MQTT_PORT
    )


    client.subscribe(
        MQTT_TOPIC
    )


    print(
        f"Backend listening on {MQTT_TOPIC}"
    )


    client.loop_forever()