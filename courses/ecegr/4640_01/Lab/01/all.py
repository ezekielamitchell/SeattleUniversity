from time import time, sleep
from urllib.request import urlopen
import urllib.error
import sys
from envirophat import motion, weather, light, analog
import math

WRITE_API = "YZS13Z5HLRLHSLP7"
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

SensorPrevSec = 0
SensorInterval = 2  # 2 seconds
ThingSpeakPrevSec = 0
ThingSpeakInterval = 20  # 20 seconds

# Initialize variables
sun = 0
logg = [0, 0, 0, 0]
temperature = 0
x, y, z = 0, 0, 0

try:
    while True:
        if time() - SensorPrevSec > SensorInterval:
            SensorPrevSec = time()

            sun = light.light()
            logg = analog.read_all()
            temperature = weather.temperature()
            x, y, z = motion.accelerometer()

        if time() - ThingSpeakPrevSec > ThingSpeakInterval:
            ThingSpeakPrevSec = time()
            thingspeakHttp = BASE_URL + "&field1={:.2f}&field2={:.2f}&field3={:.2f}&field4={:.2f}".format(temperature, sun, math.sqrt(x**2 + y**2 + z**2), logg[0])
            print(thingspeakHttp)
            conn = urlopen(thingspeakHttp)
            print("Response: {}".format(conn.read()))
            conn.close()
            sleep(1)
except KeyboardInterrupt:
    conn.close()