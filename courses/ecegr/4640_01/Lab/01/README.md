# Lab 01 - EnviroPHAT Sensor Data to ThingSpeak

This lab contains Python scripts for reading sensor data from the EnviroPHAT and uploading it to ThingSpeak.

## Setup

### Prerequisites
- Python 3.x
- EnviroPHAT library
- ThingSpeak account with channels set up

### Installation

1. Install Python dependencies from the repository root:
   ```bash
   cd /path/to/SeattleUniversity
   pip install -r requirements.txt
   ```

### API Key Configuration

**Important:** API keys are sensitive credentials and should never be committed to version control.

1. Copy the example environment file in the **repository root**:
   ```bash
   cd /path/to/SeattleUniversity
   cp .env.example .env
   ```

2. Edit the `.env` file in the repository root and add your ThingSpeak API keys:
   ```
   ECEGR_4640_01_LAB_01_THINGSPEAK_TEMPERATURE_API_KEY=your_actual_temperature_api_key
   ECEGR_4640_01_LAB_01_THINGSPEAK_MOTION_API_KEY=your_actual_motion_api_key
   ```

3. The scripts will automatically load environment variables from the repository root `.env` file using python-dotenv.

## Scripts

### temperature.py
Reads temperature data from the EnviroPHAT weather sensor and uploads to ThingSpeak.

**Required environment variable:** `ECEGR_4640_01_LAB_01_THINGSPEAK_TEMPERATURE_API_KEY`

```bash
cd courses/ecegr/4640_01/Lab/01
python temperature.py
```

### motion_detect.py
Reads accelerometer data from the EnviroPHAT motion sensor and uploads to ThingSpeak.

**Required environment variable:** `ECEGR_4640_01_LAB_01_THINGSPEAK_MOTION_API_KEY`

```bash
cd courses/ecegr/4640_01/Lab/01
python motion_detect.py
```

### all.py
Reads data from all EnviroPHAT sensors (temperature, light, motion, analog) and uploads to ThingSpeak.

**Required environment variable:** `ECEGR_4640_01_LAB_01_THINGSPEAK_MOTION_API_KEY`

```bash
cd courses/ecegr/4640_01/Lab/01
python all.py
```

## Security Notes

- All API keys are stored in a global `.env` file at the repository root
- The `.env` file is automatically excluded from git via `.gitignore`
- Never commit actual API keys to the repository
- Use `.env.example` at the repository root as a template for setting up your local environment
- Each script will raise an error if the required API key is not set
- API keys are organized by course number to avoid conflicts between different courses
