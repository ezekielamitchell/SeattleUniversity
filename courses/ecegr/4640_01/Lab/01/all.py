"""
Multi-Sensor Monitoring Script for ThingSpeak

This script reads multiple sensor data from an Enviro pHAT and uploads it to ThingSpeak.
Monitors and uploads:
    - Field 1: Temperature (degrees Celsius)
    - Field 2: Light level (lux)
    - Field 3: Acceleration magnitude (m/s²)
    - Field 4: Analog input reading

The script reads sensors every 2 seconds and uploads to ThingSpeak every 20 seconds.

Requirements:
    - envirophat library
    - python-dotenv library
    - Active ThingSpeak channel with Write API key

Setup:
    1. Copy .env.example to .env in this directory
    2. Add your ThingSpeak Write API key to the .env file
    3. Run this script with: python all.py

Author: Seattle University - ECEGR 4640
"""

from time import time, sleep
from urllib.request import urlopen
import urllib.error
import sys
import os
from envirophat import motion, weather, light, analog
import math
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
SensorInterval = 2  # Read sensors every 2 seconds
ThingSpeakPrevSec = 0
ThingSpeakInterval = 20  # Upload to ThingSpeak every 20 seconds

# Initialize sensor variables
sun = 0          # Light level in lux
logg = [0, 0, 0, 0]  # Analog input readings
temperature = 0  # Temperature in degrees Celsius
x, y, z = 0, 0, 0  # Accelerometer readings (x, y, z axes)

try:
    # Main monitoring loop
    while True:
        # Read all sensors at specified interval
        if time() - SensorPrevSec > SensorInterval:
            SensorPrevSec = time()

            # Read light sensor
            sun = light.light()
            
            # Read all analog inputs
            logg = analog.read_all()
            
            # Read temperature sensor
            temperature = weather.temperature()
            
            # Read accelerometer data
            x, y, z = motion.accelerometer()

        # Upload data to ThingSpeak at specified interval
        if time() - ThingSpeakPrevSec > ThingSpeakInterval:
            ThingSpeakPrevSec = time()
            
            # Calculate the magnitude of acceleration from x, y, z components
            accel_magnitude = math.sqrt(x**2 + y**2 + z**2)
            
            # Construct the HTTP request with all sensor data
            # field1: temperature, field2: light, field3: acceleration magnitude, field4: analog reading
            thingspeakHttp = BASE_URL + "&field1={:.2f}&field2={:.2f}&field3={:.2f}&field4={:.2f}".format(
                temperature, sun, accel_magnitude, logg[0])
            print(thingspeakHttp)
            
            # Send data to ThingSpeak
            conn = urlopen(thingspeakHttp)
            print('Response: {}', format(conn.read()))
            conn.close()
            sleep(1)
            
except KeyboardInterrupt:
    # Clean up connection on keyboard interrupt (Ctrl+C)
    print("\nShutting down gracefully...")
    conn.close()
