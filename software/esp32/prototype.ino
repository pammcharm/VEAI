// VEAI ESP32 Prototype
// Reads sensors (PIR, HC-SR04, DHT22) and sends data to Raspberry Pi via Serial.
// TODO: add full sensor code and pin mapping.

// Pin definitions - to be configured
// #define PIR_PIN 2
// #define TRIG_PIN 5
// #define ECHO_PIN 18
// #define DHT_PIN 4

// I2S pins for INMP441
// #define I2S_WS 15
// #define I2S_SCK 16
// #define I2S_SD 17

// DAC pins for speaker (PAM8403)
// #define DAC_PIN 25

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  
  // TODO: Initialize sensors
  // TODO: Configure I2S for microphone
  // TODO: Setup DAC for speaker output
  
  Serial.println("VEAI ESP32 Prototype Started");
}

void loop() {
  // TODO: Read sensor values
  // TODO: Send sensor data to Raspberry Pi via Serial
  // TODO: Handle voice input via I2S
  // TODO: Handle audio output via DAC
  
  delay(100);
}
