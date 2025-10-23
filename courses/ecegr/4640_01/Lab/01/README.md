# Lab 01 - EnviroPHAT Sensor Data to ThingSpeak

This lab contains Python scripts for reading sensor data from the EnviroPHAT and uploading it to ThingSpeak.

## Setup

### Prerequisites
- Python 3.x
- EnviroPHAT library
- ThingSpeak account with channels set up

### API Key Configuration

**Important:** API keys are sensitive credentials and should never be committed to version control.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your ThingSpeak API keys:
   ```
   THINGSPEAK_TEMPERATURE_API_KEY=your_actual_temperature_api_key
   THINGSPEAK_MOTION_API_KEY=your_actual_motion_api_key
   ```

3. Set environment variables before running the scripts:
   ```bash
   # On Linux/Mac
   export THINGSPEAK_TEMPERATURE_API_KEY=your_actual_temperature_api_key
   export THINGSPEAK_MOTION_API_KEY=your_actual_motion_api_key
   
   # Or use a tool like python-dotenv to load from .env file
   ```

## Scripts

### temperature.py
Reads temperature data from the EnviroPHAT weather sensor and uploads to ThingSpeak.

**Required environment variable:** `THINGSPEAK_TEMPERATURE_API_KEY`

```bash
python temperature.py
```

### motion_detect.py
Reads accelerometer data from the EnviroPHAT motion sensor and uploads to ThingSpeak.

**Required environment variable:** `THINGSPEAK_MOTION_API_KEY`

```bash
python motion_detect.py
```

### all.py
Reads data from all EnviroPHAT sensors (temperature, light, motion, analog) and uploads to ThingSpeak.

**Required environment variable:** `THINGSPEAK_MOTION_API_KEY`

```bash
python all.py
```

## Security Notes

- The `.env` file is automatically excluded from git via `.gitignore`
- Never commit actual API keys to the repository
- Use `.env.example` as a template for setting up your local environment
- Each script will raise an error if the required API key is not set
