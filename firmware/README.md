# VEAI Firmware

This folder contains the firmware for VEAI AI Eyes, Ears, and Voice system.

## Structure

```
firmware/
├── esp32/              # ESP32 firmware (Arduino)
│   └── firmware.ino   # Main ESP32 firmware
├── raspberry_pi/       # Raspberry Pi Python code
│   └── firmwareController.py  # Main controller
├── tools/             # Utility tools
│   └── veai_ui.py     # Web control UI
├── models/            # AI models (download during setup)
└── requirements.txt   # Python dependencies
```

## Quick Setup

### 1. Install Python Dependencies

```bash
cd firmware
pip install -r requirements.txt
```

### 2. Flash ESP32

1. Open Arduino IDE
2. Install ESP32 board support
3. Open `firmware/esp32/firmware.ino`
4. Select your ESP32 board
5. Upload

### 3. Run Raspberry Pi Controller

```bash
cd firmware/raspberry_pi
python firmwareController.py
```

### 4. Run Web UI

```bash
cd firmware/tools
python veai_ui.py
```

Then open http://localhost:8000 in your browser.

## ESP32 Pin Connections

| Component | GPIO Pin |
|-----------|----------|
| INMP441 WS | 15 |
| INMP441 SCK | 16 |
| INMP441 SD | 17 |
| PAM8403 IN | 25 (DAC) |
| PIR Sensor | 2 |
| HC-SR04 TRIG | 5 |
| HC-SR04 ECHO | 18 |
| DHT22 | 4 |

## Serial Protocol

ESP32 sends sensor data in format:
```
SENSOR:MOTION=1,DIST=10.5,TEMP=25.0,HUM=60.0
```

## Next Steps

- [ ] Install AI models to `firmware/models/`
- [ ] Add voice recognition
- [ ] Add computer vision processing
- [ ] Test full integration
