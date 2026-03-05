/**
 * VEAI Control Panel - JavaScript
 * Connects to VEAI firmware and provides real-time control
 */

// API Configuration
const API_BASE = 'http://localhost:8000';
let isConnected = false;
let pollingInterval = null;

// DOM Elements
const elements = {
    // Status
    connectionStatus: document.getElementById('connectionStatus'),
    statusText: document.getElementById('statusText'),
    connectedDevice: document.getElementById('connectedDevice'),
    
    // Sensors
    motionStatus: document.getElementById('motionStatus'),
    distanceValue: document.getElementById('distanceValue'),
    tempValue: document.getElementById('tempValue'),
    humidValue: document.getElementById('humidValue'),
    pirValue: document.getElementById('pirValue'),
    ultrasonicValue: document.getElementById('ultrasonicValue'),
    dhtTempValue: document.getElementById('dhtTempValue'),
    dhtHumValue: document.getElementById('dhtHumValue'),
    
    // Voice
    recognizedText: document.getElementById('recognizedText'),
    ttsInput: document.getElementById('ttsInput'),
    
    // Chat
    chatInput: document.getElementById('chatInput'),
    chatMessages: document.getElementById('chatMessages'),
    
    // Settings
    serialPort: document.getElementById('serialPort'),
    baudRate: document.getElementById('baudRate'),
    speechRate: document.getElementById('speechRate'),
    speechRateValue: document.getElementById('speechRateValue'),
    volume: document.getElementById('volume'),
    volumeValue: document.getElementById('volumeValue')
};

// Sensor Data
let sensorData = {
    motion: false,
    distance: 0,
    temperature: 0,
    humidity: 0
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initButtons();
    initVoice();
    initChat();
    initSettings();
    startPolling();
    
    // Simulate connection for demo
    setTimeout(() => {
        simulateConnection();
    }, 1500);
});

// Navigation
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const panels = document.querySelectorAll('.panel');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const panelId = item.dataset.panel;
            
            // Update nav
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            // Update panel
            panels.forEach(panel => panel.classList.remove('active'));
            document.getElementById(panelId).classList.add('active');
        });
    });
}

// Buttons
function initButtons() {
    // Quick actions
    document.getElementById('btnListen')?.addEventListener('click', () => sendCommand('LISTEN'));
    document.getElementById('btnSpeak')?.addEventListener('click', () => sendCommand('SPEAK'));
    document.getElementById('btnWatch')?.addEventListener('click', () => sendCommand('WATCH'));
    document.getElementById('btnIdle')?.addEventListener('click', () => sendCommand('IDLE'));
    
    // Vision buttons
    document.querySelectorAll('.vision-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.vision-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const visionType = btn.dataset.vision;
            updateVisionMode(visionType);
        });
    });
    
    // TTS button
    document.getElementById('btnTTS')?.addEventListener('click', () => {
        const text = elements.ttsInput.value;
        if (text.trim()) {
            speakText(text);
        }
    });
    
    // Settings buttons
    document.getElementById('btnConnect')?.addEventListener('click', toggleConnection);
    document.getElementById('btnReloadModels')?.addEventListener('click', reloadModels);
}

// Voice
function initVoice() {
    const recordBtn = document.getElementById('btnRecord');
    
    if (recordBtn) {
        // Mouse events
        recordBtn.addEventListener('mousedown', startRecording);
        recordBtn.addEventListener('mouseup', stopRecording);
        recordBtn.addEventListener('mouseleave', stopRecording);
        
        // Touch events
        recordBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            startRecording();
        });
        recordBtn.addEventListener('touchend', stopRecording);
    }
}

function startRecording() {
    const btn = document.getElementById('btnRecord');
    btn.classList.add('recording');
    elements.recognizedText.textContent = 'Listening...';
    
    // In real implementation, this would trigger voice recognition
    // For demo, simulate after 2 seconds
    setTimeout(() => {
        if (btn.classList.contains('recording')) {
            elements.recognizedText.textContent = 'Demo: Voice recognition would happen here';
        }
    }, 2000);
}

function stopRecording() {
    const btn = document.getElementById('btnRecord');
    btn.classList.remove('recording');
}

// Chat
function initChat() {
    const sendBtn = document.getElementById('btnSend');
    const input = elements.chatInput;
    
    if (sendBtn && input) {
        sendBtn.addEventListener('click', sendChatMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
}

function sendChatMessage() {
    const message = elements.chatInput.value.trim();
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    elements.chatInput.value = '';
    
    // Get AI response (simulated for demo)
    setTimeout(() => {
        const response = getAIResponse(message);
        addChatMessage(response, 'bot');
    }, 500);
}

function addChatMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `
        <div class="message-avatar">${sender === 'bot' ? '🤖' : '👤'}</div>
        <div class="message-content">
            <p>${text}</p>
        </div>
    `;
    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

function getAIResponse(message) {
    const responses = {
        'hello': 'Hello! How can I help you today?',
        'hi': 'Hi there! What would you like to do?',
        'who': 'I am VEAI - Voice, Eyes, and Ears Artificial Intelligence running on Raspberry Pi with ESP32.',
        'what can you do': 'I can see using the camera, hear through microphones, speak using text-to-speech, and chat with you!',
        'sensors': 'I have sensors for motion detection (PIR), distance measurement (HC-SR04), and temperature/humidity (DHT22).',
        'default': 'That\'s interesting! Ask me about my capabilities or sensors.'
    };
    
    const lower = message.toLowerCase();
    for (const [key, value] of Object.entries(responses)) {
        if (lower.includes(key)) {
            return value;
        }
    }
    return responses.default;
}

// Settings
function initSettings() {
    // Speech rate slider
    elements.speechRate?.addEventListener('input', (e) => {
        elements.speechRateValue.textContent = e.target.value;
    });
    
    // Volume slider
    elements.volume?.addEventListener('input', (e) => {
        elements.volumeValue.textContent = e.target.value + '%';
    });
}

// API Functions
async function fetchStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        if (response.ok) {
            const data = await response.json();
            updateSensorDisplay(data);
        }
    } catch (error) {
        // Silently fail - UI will show disconnected
    }
}

function updateSensorDisplay(data) {
    // Update dashboard
    elements.motionStatus.textContent = data.sensors?.motion ? 'DETECTED' : 'None';
    elements.motionStatus.style.color = data.sensors?.motion ? '#ffaa00' : '#00ff88';
    
    elements.distanceValue.textContent = (data.sensors?.distance || 0).toFixed(1) + ' cm';
    elements.tempValue.textContent = (data.sensors?.temperature || 0).toFixed(1) + '°C';
    elements.humidValue.textContent = (data.sensors?.humidity || 0).toFixed(1) + '%';
    
    // Update sensors panel
    elements.pirValue.textContent = data.sensors?.motion ? 'Active' : 'Clear';
    elements.ultrasonicValue.textContent = (data.sensors?.distance || 0).toFixed(1) + ' cm';
    elements.dhtTempValue.textContent = (data.sensors?.temperature || 0).toFixed(1) + '°C';
    elements.dhtHumValue.textContent = (data.sensors?.humidity || 0).toFixed(1) + '%';
}

async function sendCommand(command) {
    try {
        await fetch(`${API_BASE}/api/command?cmd=${command}`);
        logEvent(`Command sent: ${command}`);
    } catch (error) {
        console.error('Command failed:', error);
    }
}

async function speakText(text) {
    // In real implementation, this would trigger TTS
    logEvent(`TTS: ${text}`);
}

async function updateVisionMode(mode) {
    logEvent(`Vision mode: ${mode}`);
}

async function reloadModels() {
    logEvent('Reloading AI models...');
    // Simulate reload
    setTimeout(() => {
        logEvent('Models reloaded successfully!');
    }, 2000);
}

// Connection Management
function simulateConnection() {
    isConnected = true;
    elements.connectionStatus.classList.add('connected');
    elements.statusText.textContent = 'Connected';
    elements.connectedDevice.textContent = 'VEAI ESP32 + RPi';
    
    // Simulate sensor updates
    startSensorSimulation();
}

function toggleConnection() {
    if (isConnected) {
        disconnect();
    } else {
        connect();
    }
}

function connect() {
    elements.statusText.textContent = 'Connecting...';
    
    // Simulate connection
    setTimeout(() => {
        simulateConnection();
    }, 1000);
}

function disconnect() {
    isConnected = false;
    elements.connectionStatus.classList.remove('connected');
    elements.statusText.textContent = 'Disconnected';
    elements.connectedDevice.textContent = 'None';
    
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

// Polling
function startPolling() {
    pollingInterval = setInterval(() => {
        if (isConnected) {
            fetchStatus();
        }
    }, 2000);
}

// Event Logging
function logEvent(message) {
    console.log(`[VEAI] ${message}`);
}

// Sensor Simulation (for demo when not connected to real hardware)
function startSensorSimulation() {
    setInterval(() => {
        if (isConnected) {
            // Random sensor values for demo
            const data = {
                sensors: {
                    motion: Math.random() > 0.7,
                    distance: Math.random() * 100,
                    temperature: 20 + Math.random() * 10,
                    humidity: 40 + Math.random() * 30
                }
            };
            updateSensorDisplay(data);
        }
    }, 3000);
}

// Export for potential module use
window.VEAI = {
    sendCommand,
    speakText,
    getAIResponse
};
