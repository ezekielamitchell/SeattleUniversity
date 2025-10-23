from time import time, sleep
from urllib.request import urlopen
import urllib.error
import sys
from envirophat import weather, leds

WRITE_API = "TJ2D3LRDO4A4BEVO"  # Replace your ThingSpeak API key here
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

SensorPrevSec = 0
SensorInterval = 2  # 2 seconds
ThingSpeakPrevSec = 0
ThingSpeakInterval = 20  # 20 seconds
temperature = weather.temperature()


try:
    while True:
        if time() - SensorPrevSec > SensorInterval:
            SensorPrevSec = time()

            temperature = weather.temperature()
            print("{} degrees Celcius".format(temperature))

        if time() - ThingSpeakPrevSec > ThingSpeakInterval:
            ThingSpeakPrevSec = time()
            thingspeakHttp = BASE_URL + "&field1={:.2f}".format(temperature)
            print(thingspeakHttp)
            conn = urlopen(thingspeakHttp)
            print("Response: {}".format(conn.read()))
            conn.close()
            sleep(1)
except KeyboardInterrupt:
    conn.close()