# VEAI — Voice & Eyes & Ears Artificial Intelligence

VEAI is a local AI interaction device that can **see, hear, and respond** in real time.
It uses a **Raspberry Pi** for AI processing (Python/OpenCV/voice logic) and an **ESP32** for real-time sensor and hardware control.

## Features (Prototype Goals)
- Camera vision input (Pi Camera)
- Microphone input (INMP441)
- Speaker output (PAM8403 + 3W speaker)
- Sensors: motion (PIR), distance (HC-SR04), temperature/humidity (DHT22)
- ESP32 sends real-time sensor data to Raspberry Pi over Serial/UART

## Repo Structure
- `design/` — Cirkit Designer project files, diagrams, screenshots
- `hardware/` — wiring notes and BOM
- `software/esp32/` — ESP32 firmware
- `software/raspberry_pi/` — Python code for Raspberry Pi AI logic
- `docs/` — build notes and journal entries

## Design Files
See `design/cirkit/` and `design/screenshots/` for the circuit design.

## Hardware Overview

### AI Eyes (Vision)
- **Pi Camera** - Captures visual input for AI processing
- Connected to Raspberry Pi via CSI interface

### AI Ears (Audio Input)
- **INMP441** - High-performance MEMS microphone
- I2S interface for digital audio output

### AI Voice (Audio Output)
- **PAM8403** - Class D audio amplifier
- **3W Speaker** - Voice output

### Sensors
- **HC-SR04** - Ultrasonic distance sensor
- **PIR** - Passive infrared motion sensor
- **DHT22** - Temperature and humidity sensor

### Control
- **ESP32** - Real-time sensor reading and hardware control
- Communicates with Raspberry Pi via UART/Serial

## Next Steps
1. Finish ESP32 sensor firmware
2. Raspberry Pi serial reader prototype
3. Add basic voice output and simple vision test
4. Integrate AI models for voice recognition and computer vision

## Getting Started

### Hardware Setup
1. Connect ESP32 to sensors as defined in hardware/wiring/
2. Connect Pi Camera to Raspberry Pi
3. Wire INMP441 to ESP32 (I2S)
4. Connect PAM8403 amplifier to ESP32 DAC
5. Power ESP32 via USB, Raspberry Pi via USB-C

### Software Setup
1. Flash ESP32 with firmware from software/esp32/
2. Install Python dependencies on Raspberry Pi
3. Run the main Python script

## License
MIT License
