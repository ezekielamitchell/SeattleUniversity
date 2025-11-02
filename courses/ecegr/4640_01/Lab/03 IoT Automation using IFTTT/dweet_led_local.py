# local version of dweet_led.py
import signal
import json
import os
import sys
import logging
from time import sleep
from uuid import uuid1
import requests
from envirophat import weather, leds                                                                    


# Global Variables
THING_NAME_FILE = 'thing_name.txt'  # The name of our "thing" is persisted into this file
LOCAL_DWEET_SERVER = 'http://localhost:5000'  # Local dweet server URL
URL = LOCAL_DWEET_SERVER            # Use local server instead of dweet.io
last_led_state = None               # Current state of LED ("on", "off", "blinking")
thing_name = None                   # Thing name (as persisted in THING_NAME_FILE)


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


leds.off()

def resolve_thing_name(thing_file):
    """Get existing, or create a new thing name"""
    if os.path.exists(thing_file):
        with open(thing_file, 'r') as file_handle:
            name = file_handle.read()
            logger.info('Thing name ' + name + ' loaded from ' + thing_file)
            return name.strip()
    else:
        name = str(uuid1())[:8]  # UUID object to string.
        logger.info('Created new thing name ' + name)

        with open(thing_file, 'w') as f:
            f.write(name)

    return name


def get_latest_dweet():
    """Get the last dweet made by our thing."""
    resource = URL + '/get/latest/dweet/for/' + thing_name
    logger.debug('Getting last dweet from url %s', resource)

    try:
        r = requests.get(resource, timeout=5)  # Add timeout for local server

        if r.status_code == 200:
            dweet = r.json() # return a Python dict.
            logger.debug('Last dweet for thing was %s', dweet)

            dweet_content = None

            if dweet['this'] == 'succeeded':
                # Check if there are any dweets
                if dweet['with'] and len(dweet['with']) > 0:
                    # We're just interested in the dweet content property.
                    dweet_content = dweet['with'][0]['content']

            return dweet_content

        else:
            logger.error('Getting last dweet failed with http status %s', r.status_code)
            return {}
            
    except requests.exceptions.ConnectionError:
        logger.warning('Cannot connect to local dweet server. Is it running?')
        logger.info('Start the server with: python local_dweet_server.py')
        return {}
    except Exception as e:
        logger.error('Error getting dweet: %s', e)
        return {}


def poll_dweets_forever(delay_secs=2):
    """Poll local dweet server for dweets about our thing."""
    while True:
        dweet = get_latest_dweet()
        if dweet is not None:
            process_dweet(dweet)
        
        sleep(delay_secs)


def process_dweet(dweet):
    """Inspect the dweet and set LED state accordingly"""
    global last_led_state

    if not 'state' in dweet:
        return

    led_state = dweet['state'].lower().strip()

    if led_state == last_led_state:
        return; # LED is already in requested state.

    if led_state == 'on':
        leds.on()
    else: # Off, including any unhandled state.
        led_state = 'off'
        leds.off()

    if led_state != last_led_state:
        last_led_state = led_state
        logger.info('LED ' + led_state)


def print_instructions():
    """Print instructions to terminal."""
    print("🔴 LED Control URLs - Try them in your web browser:")
    print("  On    : " + URL + "/dweet/for/" + thing_name + "?state=on")
    print("  Off   : " + URL + "/dweet/for/" + thing_name + "?state=off")
    print("  Status: " + URL + "/get/latest/dweet/for/" + thing_name)
    print("\n💡 Local Dweet Server Commands:")
    print("  Start server: python local_dweet_server.py")
    print("  Test with curl:")
    print("    curl \"" + URL + "/dweet/for/" + thing_name + "?state=on\"")
    print("    curl \"" + URL + "/dweet/for/" + thing_name + "?state=off\"")


def signal_handler(sig, frame):
    """Release resources and clean up as needed."""
    print('You pressed Control+C')
    leds.off()
    sys.exit(0)


# Initialise Module
thing_name = resolve_thing_name(THING_NAME_FILE)
leds.off()

# Main entry point
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # Capture CTRL + C
    print("🏠 Local LED Control System")
    print_instructions()

    # Test connection to local server
    logger.info("Testing connection to local dweet server...")
    test_dweet = get_latest_dweet()
    if test_dweet is None:
        print("\n⚠️  Warning: Cannot connect to local dweet server!")
        print("   Please start it first: python local_dweet_server.py")
        print("   Then run this script again.")
        sys.exit(1)
    else:
        print("✅ Connected to local dweet server!")

    # Initialise LED from last dweet.
    last_dweet = get_latest_dweet()
    if (last_dweet):
        process_dweet(last_dweet)

    print('\n🔄 Waiting for dweets. Press Control+C to exit.')
    poll_dweets_forever() # Get dweets by polling the local server