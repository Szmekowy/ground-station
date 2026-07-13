import json
import time
import random
import paho.mqtt.client as mqtt


MQTT_BROKER = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "balloon/raw"

SEND_INTERVAL = 1  # sekundy


client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)


def generate_test_data(): #Generuje testowe dane // w Przyszłosći zamiast tej funkcji będzie funckja odbierająca dane z balona 
    
    data = {
        "timestamp": time.time(),
        "position": {
            "x": round(random.uniform(0, 100), 2),
            "y": round(random.uniform(0, 100), 2),
            "z": round(random.uniform(0, 500), 2)
        },

        "battery": round(random.uniform(50, 100), 2),
        "pressure": round(random.uniform(950, 1050), 2)
    }

    return data


def publish_test_data(): #publikuje testowe dane do backendu  // w przyszlosci zamiast test beda zwykle dane 

    while True:

        data = generate_test_data()

        json_data = json.dumps(data)

        client.publish(
            MQTT_TOPIC,
            json_data
        )

        print("Published:", json_data)

        time.sleep(SEND_INTERVAL)


if __name__ == "__main__":
    publish_test_data()