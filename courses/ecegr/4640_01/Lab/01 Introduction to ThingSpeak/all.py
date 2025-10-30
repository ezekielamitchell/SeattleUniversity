from time import time, sleep
from urllib.request import urlopen
import urllib.error
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from envirophat import motion, weather, light, analog
import math

# Load environment variables from repository root .env file
repo_root = Path(__file__).resolve().parents[5]
dotenv_path = repo_root / '.env'
load_dotenv(dotenv_path)

# Load API key from environment variable
WRITE_API = os.getenv("ECEGR_4640_01_LAB_01_THINGSPEAK_MOTION_API_KEY")
if not WRITE_API:
    raise ValueError("ECEGR_4640_01_LAB_01_THINGSPEAK_MOTION_API_KEY environment variable is not set. Please create a .env file in the repository root using .env.example as a template.")

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