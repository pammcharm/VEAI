# VEAI - Voice, Eyes & Ears Artificial Intelligence

![VEAI Logo](logo.png)

## Project Overview

VEAI is a local AI-powered robot that can see, hear, and speak in real-time. It uses a Raspberry Pi for AI processing and an ESP32 for real-time sensor control.

## What Can VEAI Do?

### AI Eyes (Vision)
- Object detection using AI models
- Face recognition
- Hand tracking
- Pose estimation
- Real-time camera feed

### AI Ears (Hearing)
- Speech recognition (Whisper/Vosk)
- Voice command processing
- Audio capture via I2S microphone

### AI Voice (Speaking)
- Text-to-speech output
- Interactive chatbot
- Voice responses

### Sensors
- PIR - Motion detection
- HC-SR04 - Distance measurement
- DHT22 - Temperature & humidity

## Project Structure

```
VEAI/
├── README.md           # This file
├── BUDGET.md          # Budget plan ($400)
├── PROJECT.md         # Full documentation
├── logo.png           # Project logo
│
├── design/            # Circuit design files
│   ├── cirkit/        # Cirkit Designer project
│   ├── diagrams/      # Circuit diagrams
│   └── screenshots/   # Design screenshots
│
├── firmware/          # All firmware & code
│   ├── esp32/         # ESP32 Arduino code
│   ├── raspberry_pi/  # Python controller
│   ├── models/        # AI models (installable)
│   ├── tools/         # Utilities & Web UI
│   └── requirements.txt
│
├── gui/               # Web control panel
│   ├── index.html     # Main UI
│   ├── css/          # Styles
│   └── js/            # JavaScript
│
├── hardware/          # Hardware documentation
│   ├── bom/          # Bill of materials
│   └── wiring/       # Wiring diagrams
│
├── software/          # Legacy software folder
│   ├── esp32/
│   └── raspberry_pi/
│
└── docs/             # Documentation
    └── journal/      # Build notes
```

## Hardware Required

### Core Components

See BUDGET.md for full breakdown - Total: $400

| Category | Components |
|----------|------------|
| Computing | Laptop ($220), Raspberry Pi 4 ($55), ESP32 ($10), SD Card ($12), Power ($10) |
| AI Eyes | Pi Camera v2 ($25), Camera Cable ($5) |
| AI Ears | INMP441 Microphone ($6), Jumper Wires ($2) |
| AI Voice | PAM8403 Amp ($5), 3W Speaker ($6), Audio Cables ($3) |
| Sensors | HC-SR04 ($4), PIR ($3), DHT22 ($5) |
| Misc | Power Strip, Cables, Breadboard, Case, etc. |

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/pammcharm/VEAI.git
cd VEAI
```

### 2. Install Raspberry Pi Software
```bash
# Install dependencies
cd firmware
pip install -r requirements.txt

# Install AI models (optional)
cd models
python install_models.py quick
```

### 3. Flash ESP32
1. Open Arduino IDE
2. Install ESP32 board support
3. Open firmware/esp32/firmware.ino
4. Upload to ESP32

### 4. Run the System
```bash
# Start Raspberry Pi controller
cd firmware/raspberry_pi
python firmwareController.py

# In another terminal, start Web UI
cd firmware/tools
python veai_ui.py
```

### 5. Open Control Panel
Navigate to: http://localhost:8000

## GUI Control Panel

The web-based control panel includes:

- Dashboard - Real-time sensor readings, quick actions
- AI Vision - Object detection, face, hand, pose modes
- AI Voice - Voice recording and TTS
- Sensors - All sensor readings
- Chat - Talk to VEAI's NLP brain
- Settings - Configure connection and models

## Software Components

### ESP32 Firmware
- I2S microphone input
- DAC audio output
- Sensor readings (PIR, HC-SR04, DHT22)
- Serial communication

### Raspberry Pi Controller
- Serial communication with ESP32
- Camera capture
- AI model integration
- State management

### AI Models
- Voice: Whisper, Vosk, pyttsx3
- Vision: MediaPipe, OpenCV DNN
- NLP: Transformers, rule-based fallback

## Pin Connections

### ESP32 Pinout

| Component | GPIO |
|-----------|------|
| INMP441 WS | 15 |
| INMP441 SCK | 16 |
| INMP441 SD | 17 |
| PAM8403 IN | 25 |
| PIR Sensor | 2 |
| HC-SR04 TRIG | 5 |
| HC-SR04 ECHO | 18 |
| DHT22 | 4 |

## Development

### Running the GUI
```bash
cd firmware/tools
python veai_ui.py
```

### Testing AI Models
```bash
cd firmware/models
python veai_models.py
```

### Installing All Models
```bash
cd firmware/models
python install_models.py all
```

## Build Journal

See docs/journal/ for build progress and notes.

## Contributing

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - Feel free to use and modify!

## Acknowledgments

- OpenAI Whisper
- MediaPipe
- HuggingFace Transformers
- Raspberry Pi Foundation
- Espressif (ESP32)

---

VEAI - Your Personal AI Companion

Built with Raspberry Pi + ESP32
