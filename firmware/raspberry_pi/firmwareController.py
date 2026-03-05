#!/usr/bin/env python3
"""
VEAI Raspberry Pi Firmware Controller
AI Brain - Processes vision, hearing, and controls voice output

Features:
- Serial communication with ESP32
- Camera vision input (Pi Camera)
- Voice input/output processing
- AI model integration
- Web UI for control
"""

import serial
import time
import threading
import json
import logging
from datetime import datetime
from enum import Enum

# Try to import optional dependencies
try:
    import cv2
    from picamera2 import Picamera2
    CAMERA_AVAILABLE = True
except ImportError:
    CAMERA_AVAILABLE = False
    logging.warning("Camera not available")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Configuration
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
HTTP_PORT = 8000

class VEAIState(Enum):
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    WATCHING = "watching"

class SensorData:
    def __init__(self):
        self.motion = False
        self.distance = 0.0
        self.temperature = 0.0
        self.humidity = 0.0
        self.timestamp = None
        
    def update(self, motion=None, distance=None, temperature=None, humidity=None):
        if motion is not None:
            self.motion = motion
        if distance is not None:
            self.distance = distance
        if temperature is not None:
            self.temperature = temperature
        if humidity is not None:
            self.humidity = humidity
        self.timestamp = datetime.now()
        
    def to_dict(self):
        return {
            "motion": self.motion,
            "distance": self.distance,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

class VEAIFirmware:
    def __init__(self):
        self.state = VEAIState.IDLE
        self.sensor_data = SensorData()
        self.serial_conn = None
        self.running = False
        self.camera = None
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('VEAI')
        
    def connect_serial(self):
        """Connect to ESP32 via serial"""
        try:
            self.serial_conn = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # Wait for ESP32 reset
            self.logger.info(f"Connected to ESP32 on {SERIAL_PORT}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Serial connection failed: {e}")
            return False
    
    def init_camera(self):
        """Initialize Pi Camera"""
        if not CAMERA_AVAILABLE:
            self.logger.warning("Camera libraries not available")
            return False
            
        try:
            self.camera = Picamera2()
            self.camera.configure(self.camera.create_still_configuration())
            self.camera.start()
            self.logger.info("Camera initialized")
            return True
        except Exception as e:
            self.logger.error(f"Camera init failed: {e}")
            return False
    
    def parse_sensor_line(self, line):
        """Parse sensor data from ESP32"""
        if not line.startswith("SENSOR:"):
            return None
            
        try:
            # Format: SENSOR:MOTION=1,DIST=10.5,TEMP=25.0,HUM=60.0
            data = line[7:]  # Remove "SENSOR:"
            parts = data.split(',')
            
            sensor_dict = {}
            for part in parts:
                key, value = part.split('=')
                if key == "MOTION":
                    sensor_dict['motion'] = value == '1'
                elif key == "DIST":
                    sensor_dict['distance'] = float(value)
                elif key == "TEMP":
                    sensor_dict['temperature'] = float(value)
                elif key == "HUM":
                    sensor_dict['humidity'] = float(value)
                    
            self.sensor_data.update(**sensor_dict)
            return sensor_dict
            
        except Exception as e:
            self.logger.error(f"Failed to parse sensor data: {e}")
            return None
    
    def read_serial(self):
        """Read serial data from ESP32 (runs in background thread)"""
        while self.running:
            try:
                if self.serial_conn and self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8').strip()
                    if line:
                        self.logger.debug(f"Serial: {line}")
                        self.parse_sensor_line(line)
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Serial read error: {e}")
                time.sleep(1)
    
    def capture_image(self):
        """Capture image from camera"""
        if not self.camera:
            return None
            
        try:
            image = self.camera.capture_array()
            return image
        except Exception as e:
            self.logger.error(f"Capture failed: {e}")
            return None
    
    def process_vision(self):
        """Process camera vision (placeholder for AI)"""
        if not CAMERA_AVAILABLE:
            return None
            
        image = self.capture_image()
        if image is None:
            return None
            
        # TODO: Add actual AI vision processing
        # - Object detection
        # - Face recognition
        # - Motion detection
        
        return {
            "width": image.shape[1],
            "height": image.shape[0],
            "channels": image.shape[2] if len(image.shape) > 2 else 1
        }
    
    def send_command(self, command):
        """Send command to ESP32"""
        if self.serial_conn:
            try:
                self.serial_conn.write(f"{command}\n".encode())
                self.logger.info(f"Sent command: {command}")
                return True
            except Exception as e:
                self.logger.error(f"Command send failed: {e}")
                return False
        return False
    
    def start(self):
        """Start VEAI firmware"""
        self.logger.info("Starting VEAI Firmware...")
        self.running = True
        
        # Connect to ESP32
        if not self.connect_serial():
            self.logger.warning("Continuing without ESP32 connection")
        
        # Initialize camera
        if not self.init_camera():
            self.logger.warning("Continuing without camera")
        
        # Start serial read thread
        self.serial_thread = threading.Thread(target=self.read_serial, daemon=True)
        self.serial_thread.start()
        
        self.logger.info("VEAI Firmware Started!")
        
    def stop(self):
        """Stop VEAI firmware"""
        self.logger.info("Stopping VEAI Firmware...")
        self.running = False
        
        if self.serial_conn:
            self.serial_conn.close()
            
        self.logger.info("VEAI Firmware Stopped")
    
    def get_status(self):
        """Get current status"""
        return {
            "state": self.state.value,
            "sensors": self.sensor_data.to_dict(),
            "camera": self.camera is not None,
            "serial": self.serial_conn is not None and self.serial_conn.is_open
        }

# ==================== MAIN ====================

def main():
    """Main entry point"""
    veai = VEAIFirmware()
    
    try:
        veai.start()
        
        # Main loop
        while True:
            # Print sensor data
            print(f"\rSensors: Motion={veai.sensor_data.motion}, "
                  f"Dist={veai.sensor_data.distance:.1f}cm, "
                  f"Temp={veai.sensor_data.temperature:.1f}C, "
                  f"Hum={veai.sensor_data.humidity:.1f}%", end="")
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        veai.stop()

if __name__ == "__main__":
    main()
