# SeattleUniversity
A repository for my undergraduate degree

## Setup

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ezekielamitchell/SeattleUniversity.git
   cd SeattleUniversity
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### API Key Configuration

Some coursework requires API keys for external services. These are managed through a global `.env` file.

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace placeholder values with your actual API keys.

3. The `.env` file is excluded from version control via `.gitignore` to protect your credentials.

**Note:** API keys are organized by course number using the naming convention:
```
<COURSE>_<NUMBER>_<LAB/ASSIGNMENT>_<SERVICE>_<PURPOSE>_API_KEY
```

For example:
- `ECEGR_4640_01_LAB_01_THINGSPEAK_TEMPERATURE_API_KEY`
- `ECEGR_4640_01_LAB_01_THINGSPEAK_MOTION_API_KEY`

## Courses

### CPSC 2430 - Data Structures
- Week 01: C++ Basics
- Week 02: Dynamic Arrays and Templates
- Week 03: Binary Search Trees

### ECEGR 4640-01 - Embedded Systems
- Lab 01: EnviroPHAT Sensor Data to ThingSpeak

## Security

- Never commit API keys or other sensitive credentials to the repository
- Always use the `.env` file for storing secrets
- The `.env` file is automatically excluded from git via `.gitignore`
