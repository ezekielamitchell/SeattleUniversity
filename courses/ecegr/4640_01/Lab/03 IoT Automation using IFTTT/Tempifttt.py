#!/usr/bin/env python

import time
import requests
import logging

from envirophat import weather, leds
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# How often we check the temperature
POLL_INTERVAL_SECS = 60*10  # 10 Minutes

# Celsius or Fahrenheit
USE_DEGREES_CELSIUS = True                                                                     # (3)

# At what high temperature will we send an email
HIGH_TEMP_TRIGGER = 20 # Degrees                                                               # (4)

# At what low temperature will we send an email
LOW_TEMP_TRIGGER = 19  # Degrees                                                               # (5)

# To track when a high temp event has been triggered
triggered_high = False


# IFTTT Configuration
EVENT = "Event name" # <<<< Add your IFTTT Event name                                      # (6)
API_KEY = "Your key" # <<<< Add your IFTTT API Key

# Create the IFTTT Webhook URL
URL = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(EVENT, API_KEY)                  # (7)

# HTTP headers used with Webhook request.
REQUEST_HEADERS = {"Content-Type": "application/json"}

temperature = weather.temperature()
pressure = weather.pressure()

def send_ifttt_event(temperature, humidity, message):
    """ Call the IFFF Webhook URL """

    # In IFTTT, the dict/JSON key names must be value1, value2 and value3
    data = {
      "value1": temperature,
      "value2": pressure,
      "value3": message
    }

    # Make IFTTT request - it can be either a HTTP GET or POST
    response = requests.post(URL, headers=REQUEST_HEADERS, params=data)

    # IFTTT Response is plain text
    logger.info("Response {}".format(response.text))

    if response.status_code == requests.codes.ok:
        logger.info("Successful Request.")
    else:
        logger.info("Unsuccessful Request. Code:{}".format(response.status_code))
		
if __name__ == "__main__":

    try:
        logger.info("Press Control + C To Exit.")

        while True:
            try:
                result = weather.temperature() # Singe data read (faster)
                result1= weather.pressure()

            except Exception as e:
                # Failed to get reading from sensor
                logger.error("Failed to read sensor. Error: {}".format(e), exc_info=True)
                continue


            # We have a reading, eg {'temp_c': 19, 'temp_f': 66.2, 'humidity': 32, 'valid': True}
            logger.info("Sensor result {}".format(result))

            current_temp = result


            pressure = result1

            if not triggered_high and current_temp >= HIGH_TEMP_TRIGGER:
                # Trigger IFTTT Event (eg that will send email)
                logger.info("Temperature {} is >= {}, triggering event {}".format(current_temp, HIGH_TEMP_TRIGGER, EVENT))
                triggered_high = True
                send_ifttt_event(current_temp, pressure, "High Temperature Trigger")

            elif triggered_high and current_temp <= LOW_TEMP_TRIGGER:
                # Temperature is at or below low trigger threshold.
                logger.info("Temperature {} is <= {}, trigger reset".format(current_temp, LOW_TEMP_TRIGGER))
                triggered_high = False
                send_ifttt_event(current_temp, pressure, "Low Temperature Trigger")

            sleep(POLL_INTERVAL_SECS)

    except KeyboardInterrupt:
        print("Bye")