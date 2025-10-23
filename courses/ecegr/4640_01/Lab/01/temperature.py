"""
Temperature Monitoring Script for ThingSpeak

This script reads temperature data from an Enviro pHAT sensor and uploads it to ThingSpeak.
The script reads temperature every 2 seconds and uploads to ThingSpeak every 20 seconds.

Requirements:
    - envirophat library
    - python-dotenv library
    - Active ThingSpeak channel with Write API key

Setup:
    1. Copy .env.example to .env in this directory
    2. Add your ThingSpeak Write API key to the .env file
    3. Run this script with: python temperature.py

Author: Seattle University - ECEGR 4640
"""

from time import time, sleep
from urllib.request import urlopen
import urllib.error
import sys
import os
from envirophat import weather, leds
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable for security
# This prevents the API key from being committed to version control
WRITE_API = os.getenv('THINGSPEAK_WRITE_API_KEY')

# Validate that the API key is configured
if not WRITE_API:
    raise ValueError("THINGSPEAK_WRITE_API_KEY not found in environment variables. "
                     "Please create a .env file with your API key. "
                     "See .env.example for reference.")

# Construct the base URL for ThingSpeak API
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

# Timing configuration
SensorPrevSec = 0
SensorInterval = 2  # Read sensor every 2 seconds
ThingSpeakPrevSec = 0
ThingSpeakInterval = 20  # Upload to ThingSpeak every 20 seconds

# Initialize temperature variable
temperature = weather.temperature()


try:
    # Main monitoring loop
    while True:
        # Read sensor at specified interval
        if time() - SensorPrevSec > SensorInterval:
            SensorPrevSec = time()

            # Read current temperature from the Enviro pHAT sensor
            temperature = weather.temperature()
            print("{} degrees Celcius".format(temperature))

        # Upload data to ThingSpeak at specified interval
        if time() - ThingSpeakPrevSec > ThingSpeakInterval:
            ThingSpeakPrevSec = time()
            
            # Construct the HTTP request with temperature data in field1
            thingspeakHttp = BASE_URL + "&field1={:.2f}".format(temperature)
            print(thingspeakHttp)
            
            # Send data to ThingSpeak
            conn = urlopen(thingspeakHttp)
            print("Response: {}".format(conn.read()))
            conn.close()
            sleep(1)
            
except KeyboardInterrupt:
    # Clean up connection on keyboard interrupt (Ctrl+C)
    print("\nShutting down gracefully...")
    conn.close()
