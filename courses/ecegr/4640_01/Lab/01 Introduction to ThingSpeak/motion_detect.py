from time import time, sleep
from urllib.request import urlopen
import urllib.error
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from envirophat import motion
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
x, y, z = 0, 0, 0

try:
    while True:
        if time() - SensorPrevSec > SensorInterval:
            SensorPrevSec = time()

            x, y, z = motion.accelerometer()
            magnitude = math.sqrt(x**2 + y**2 + z**2)
            print("Accelerometer: x={:.2f}, y={:.2f}, z={:.2f}, magnitude={:.2f}".format(x, y, z, magnitude))

        if time() - ThingSpeakPrevSec > ThingSpeakInterval:
            ThingSpeakPrevSec = time()
            magnitude = math.sqrt(x**2 + y**2 + z**2)
            thingspeakHttp = BASE_URL + "&field1={:.2f}".format(magnitude)
            print(thingspeakHttp)
            conn = urlopen(thingspeakHttp)
            print("Response: {}".format(conn.read()))
            conn.close()
            sleep(1)
except KeyboardInterrupt:
    conn.close()
