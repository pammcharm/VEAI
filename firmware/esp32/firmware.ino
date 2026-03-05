/**
 * VEAI ESP32 Firmware
 * AI Eyes, Ears, and Voice Controller
 * 
 * Features:
 * - I2S Microphone (INMP441) for AI Ears
 * - DAC Audio Output for AI Voice (PAM8403)
 * - Sensors: PIR, HC-SR04, DHT22
 * - Serial communication with Raspberry Pi
 */

#include <Arduino.h>
#include <driver/dac.h>
#include <driver/i2s.h>
#include <DHT.h>

// ==================== PINS ====================

// I2S Microphone (INMP441)
#define I2S_WS    15
#define I2S_SCK   16
#define I2S_SD    17

// DAC Output (PAM8403)
#define DAC_PIN   25

// Sensors
#define PIR_PIN   2
#define TRIG_PIN  5
#define ECHO_PIN  18
#define DHT_PIN   4

// ==================== CONFIG ====================

#define SENSOR_READ_INTERVAL  1000  // ms
#define AUDIO_BUFFER_SIZE     256

// ==================== GLOBALS ====================

DHT dht(DHT_PIN, DHT22);
unsigned long lastSensorRead = 0;

// Sensor values
bool motionDetected = false;
float distance = 0;
float temperature = 0;
float humidity = 0;

// Audio buffer for I2S
int16_t audioBuffer[AUDIO_BUFFER_SIZE];

// ==================== SETUP ====================

void setup() {
  Serial.begin(115200);
  
  // Initialize sensors
  initSensors();
  
  // Initialize I2S for microphone
  initI2SMicrophone();
  
  // Initialize DAC for speaker
  initDAC();
  
  Serial.println("VEAI ESP32 Firmware Started");
  Serial.println("Waiting for sensors to stabilize...");
  delay(2000);
}

// ==================== LOOP ====================

void loop() {
  unsigned long currentMillis = millis();
  
  // Read sensors every interval
  if (currentMillis - lastSensorRead >= SENSOR_READ_INTERVAL) {
    readSensors();
    sendSensorData();
    lastSensorRead = currentMillis;
  }
  
  // Read microphone data
  readMicrophone();
  
  delay(10);
}

// ==================== SENSORS ====================

void initSensors() {
  // PIR Motion Sensor
  pinMode(PIR_PIN, INPUT);
  
  // HC-SR04 Ultrasonic
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  
  // DHT22
  dht.begin();
}

void readSensors() {
  // Read PIR
  motionDetected = digitalRead(PIR_PIN) == HIGH;
  
  // Read HC-SR04
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  distance = (duration * 0.034) / 2;
  
  // Read DHT22
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  
  // Validate readings
  if (isnan(temperature)) temperature = 0;
  if (isnan(humidity)) humidity = 0;
}

void sendSensorData() {
  Serial.print("SENSOR:");
  Serial.print("MOTION=");
  Serial.print(motionDetected ? 1 : 0);
  Serial.print(",DIST=");
  Serial.print(distance);
  Serial.print(",TEMP=");
  Serial.print(temperature);
  Serial.print(",HUM=");
  Serial.println(humidity);
}

// ==================== I2S MICROPHONE ====================

void initI2SMicrophone() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 1024,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };
  
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };
  
  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

void readMicrophone() {
  size_t bytesRead = 0;
  i2s_read(I2S_NUM_0, audioBuffer, sizeof(audioBuffer), &bytesRead, 0);
  
  if (bytesRead > 0) {
    // TODO: Process audio data
    // Send to Raspberry Pi or process locally
  }
}

// ==================== DAC AUDIO OUTPUT ====================

void initDAC() {
  dac_output_enable(DAC_CHANNEL_1);
  dac_output_voltage(DAC_CHANNEL_1, 0);
}

void playTone(uint8_t volume) {
  // Simple tone generation for testing
  for (int i = 0; i < 100; i++) {
    dac_output_voltage(DAC_CHANNEL_1, volume);
    delayMicroseconds(500);
    dac_output_voltage(DAC_CHANNEL_1, 0);
    delayMicroseconds(500);
  }
}

void playAudioSample(const uint8_t* data, size_t length) {
  for (size_t i = 0; i < length; i++) {
    dac_output_voltage(DAC_CHANNEL_1, data[i]);
    delayMicroseconds(62);  // ~16kHz sample rate
  }
}
