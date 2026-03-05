#!/usr/bin/env python3
"""
VEAI Raspberry Pi Prototype
Reads sensor lines from ESP32 over serial and prints / triggers simple actions.
TODO: add full serial parsing + voice output + computer vision.
"""

import serial
import time
import sys

# Serial configuration
SERIAL_PORT = '/dev/ttyUSB0'  # May vary: /dev/ttyUSB0, /dev/ttyACM0
BAUD_RATE = 115200

def main():
    """Main function to read serial data from ESP32."""
    print("VEAI Raspberry Pi Prototype Started")
    print(f"Connecting to ESP32 on {SERIAL_PORT}...")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Wait for ESP32 to reset
        
        print("Connected! Reading sensor data...")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    print(f"Sensor Data: {line}")
                    # TODO: Parse sensor data and trigger actions
                    # TODO: Add voice output using TTS
                    # TODO: Add computer vision processing
            
            time.sleep(0.1)
            
    except serial.SerialException as e:
        print(f"Error: {e}")
        print("Make sure ESP32 is connected and you have permission to access the serial port.")
        print("Try: sudo usermod -a -G dialout $USER")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()
