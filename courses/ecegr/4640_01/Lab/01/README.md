# ECEGR 4640 Lab 01 - Enviro pHAT Sensor Monitoring

This lab contains Python scripts for monitoring environmental sensors using the Pimoroni Enviro pHAT and uploading data to ThingSpeak.

## Overview

The Enviro pHAT is a sensor board for Raspberry Pi that includes:
- Temperature sensor
- Light sensor
- Motion sensor (accelerometer)
- Analog inputs

This lab includes scripts to read these sensors and upload the data to ThingSpeak for cloud monitoring and visualization.

## Prerequisites

### Hardware
- Raspberry Pi with Enviro pHAT attached
- Internet connection

### Software Dependencies
Install the required Python packages:

```bash
pip install envirophat python-dotenv
```

## Setup Instructions

### 1. ThingSpeak Account Setup
1. Create a free account at [ThingSpeak](https://thingspeak.com)
2. Create a new channel
3. Note your **Write API Key** from the channel settings

### 2. Environment Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your ThingSpeak Write API Key:
   ```
   THINGSPEAK_WRITE_API_KEY=your_actual_api_key_here
   ```

3. **Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Scripts

### temperature.py
Monitors temperature only and uploads to ThingSpeak field 1.

**Usage:**
```bash
python temperature.py
```

**Features:**
- Reads temperature every 2 seconds
- Uploads to ThingSpeak every 20 seconds
- Displays current temperature and upload status
- Press Ctrl+C to stop

**ThingSpeak Fields:**
- Field 1: Temperature (°C)

### all.py
Monitors all available sensors and uploads to ThingSpeak.

**Usage:**
```bash
python all.py
```

**Features:**
- Reads all sensors every 2 seconds
- Uploads to ThingSpeak every 20 seconds
- Displays upload URL and responses
- Press Ctrl+C to stop

**ThingSpeak Fields:**
- Field 1: Temperature (°C)
- Field 2: Light level (lux)
- Field 3: Acceleration magnitude (m/s²)
- Field 4: Analog input reading

### motion_detect.py
*(Currently empty - placeholder for future motion detection implementation)*

## Security Notes

- **Never commit API keys to version control**
- The `.env` file containing your API key is automatically excluded via `.gitignore`
- Always use the `.env.example` file as a template
- Keep your ThingSpeak Write API Key private

## Troubleshooting

### "THINGSPEAK_WRITE_API_KEY not found" error
- Make sure you've created a `.env` file in this directory
- Verify the file contains your API key in the correct format
- Check that the key name matches exactly: `THINGSPEAK_WRITE_API_KEY`

### Import errors
- Ensure all dependencies are installed: `pip install envirophat python-dotenv`
- Verify you're running on a Raspberry Pi with the Enviro pHAT attached

### No data appearing in ThingSpeak
- Verify your API key is correct
- Check your internet connection
- Ensure you're looking at the correct ThingSpeak channel
- Check the console output for error messages

## References

- [Enviro pHAT Documentation](https://learn.pimoroni.com/article/getting-started-with-enviro-phat)
- [ThingSpeak Documentation](https://www.mathworks.com/help/thingspeak/)
- [ThingSpeak API Reference](https://www.mathworks.com/help/thingspeak/rest-api.html)

## Author

Seattle University - ECEGR 4640
Embedded Systems Lab
