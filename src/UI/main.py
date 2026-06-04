import time
from ui import UI

import random
import datetime

print("UI started")

ui_module = UI()

ui_module.initialize_ui()

# testing data
temp_readings = []
alt_readings = []
location_readings = []
pressure_readings = []

gps_location = [18.606, 54.368]
temp = 20.0
altitude = 100
pressure = 1000

while True:
    temp += (random.random() * 2 - 1.0) * 0.2
    temp_reading = {
        'time': datetime.datetime.now(),
        'temp': temp
    }
    temp_readings.append(temp_reading)
    ui_module.update_temperature(temp_readings)

    altitude += random.random() * 0.5
    alt_reading = {
        'time': datetime.datetime.now(),
        'alt': altitude
    }
    alt_readings.append(alt_reading)
    ui_module.update_altitude(alt_readings)

    pressure -= random.random() * 0.4
    pressure_reading = {
        'time': datetime.datetime.now(),
        'pressure': pressure
    }
    pressure_readings.append(pressure_reading)
    ui_module.update_pressure(pressure_readings)

    gps_location[0] += (random.random() * 2 - 1.0) * 0.01
    gps_location[1] += (random.random() * 2 - 1.0) * 0.01

    location_reading = {
        'longitude': gps_location[0],
        'latitude': gps_location[1]
    }
    location_readings.append(location_reading)
    ui_module.update_location(location_readings)

    time.sleep(1)
