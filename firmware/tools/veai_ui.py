#!/usr/bin/env python3
"""
VEAI Web UI Server
Simple web interface to control VEAI
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import threading
import json
import os

# VEAI Firmware import
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from raspberry_pi.firmwareController import VEAIFirmware

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VEAI Control Center</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            background: linear-gradient(90deg, #00d4ff, #7b2cbf);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .card h3 {
            color: #00d4ff;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .sensor-value {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .sensor-label {
            color: #aaa;
            font-size: 0.9em;
        }
        .status-ok { color: #00ff88; }
        .status-warn { color: #ffaa00; }
        .status-error { color: #ff4444; }
        
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        button {
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            border: none;
            padding: 15px 25px;
            border-radius: 10px;
            color: white;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 212, 255, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        
        .log-container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
        }
        .log-entry {
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            padding: 5px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .log-timestamp {
            color: #00d4ff;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #00ff88;
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 VEAI Control Center</h1>
        
        <div class="controls">
            <button onclick="sendCommand('LISTEN')">🎤 Listen</button>
            <button onclick="sendCommand('SPEAK')">🔊 Speak</button>
            <button onclick="sendCommand('WATCH')">👁️ Watch</button>
            <button onclick="sendCommand('IDLE')">💤 Idle</button>
            <button onclick="refreshStatus()">🔄 Refresh</button>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h3><span class="live-indicator"></span>Motion</h3>
                <div class="sensor-value" id="motion">--</div>
                <div class="sensor-label">PIR Sensor</div>
            </div>
            <div class="card">
                <h3>📏 Distance</h3>
                <div class="sensor-value" id="distance">-- cm</div>
                <div class="sensor-label">HC-SR04</div>
            </div>
            <div class="card">
                <h3>🌡️ Temperature</h3>
                <div class="sensor-value" id="temperature">--°C</div>
                <div class="sensor-label">DHT22</div>
            </div>
            <div class="card">
                <h3>💧 Humidity</h3>
                <div class="sensor-value" id="humidity">--%</div>
                <div class="sensor-label">DHT22</div>
            </div>
            <div class="card">
                <h3>🔌 Status</h3>
                <div class="sensor-value" id="status">--</div>
                <div class="sensor-label">System State</div>
            </div>
            <div class="card">
                <h3>📷 Camera</h3>
                <div class="sensor-value" id="camera">--</div>
                <div class="sensor-label">Pi Camera</div>
            </div>
        </div>
        
        <div class="card">
            <h3>📝 Event Log</h3>
            <div class="log-container" id="log">
                <div class="log-entry"><span class="log-timestamp">[--:--:--]</span> VEAI UI Started</div>
            </div>
        </div>
    </div>
    
    <script>
        let lastUpdate = 0;
        
        function updateStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('motion').textContent = data.sensors.motion ? 'DETECTED' : 'None';
                    document.getElementById('motion').className = 'sensor-value ' + (data.sensors.motion ? 'status-warn' : 'status-ok');
                    
                    document.getElementById('distance').textContent = data.sensors.distance.toFixed(1) + ' cm';
                    document.getElementById('temperature').textContent = data.sensors.temperature.toFixed(1) + '°C';
                    document.getElementById('humidity').textContent = data.sensors.humidity.toFixed(1) + '%';
                    document.getElementById('status').textContent = data.state;
                    document.getElementById('camera').textContent = data.camera ? 'Ready' : 'Offline';
                })
                .catch(error => console.error('Status error:', error));
        }
        
        function sendCommand(cmd) {
            fetch('/api/command?cmd=' + cmd)
                .then(response => response.json())
                .then(data => {
                    addLog('Command sent: ' + cmd);
                    updateStatus();
                })
                .catch(error => console.error('Command error:', error));
        }
        
        function refreshStatus() {
            updateStatus();
            addLog('Status refreshed');
        }
        
        function addLog(message) {
            const now = new Date().toLocaleTimeString();
            const log = document.getElementById('log');
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = '<span class="log-timestamp">[' + now + ']</span> ' + message;
            log.insertBefore(entry, log.firstChild);
            
            // Keep only last 50 entries
            while (log.children.length > 50) {
                log.removeChild(log.lastChild);
            }
        }
        
        // Update status every 2 seconds
        setInterval(updateStatus, 2000);
        updateStatus();
    </script>
</body>
</html>
"""

class VEAHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for VEAI"""
    
    def __init__(self, *args, veai_firmware=None, **kwargs):
        self.veai = veai_firmware
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = self.veai.get_status() if self.veai else {}
            self.wfile.write(json.dumps(status).encode())
        elif self.path.startswith('/api/command'):
            cmd = self.path.split('=')[1] if '=' in self.path else ''
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            if self.veai:
                self.veai.send_command(cmd)
            self.wfile.write(json.dumps({'success': True, 'command': cmd}).encode())
        else:
            # Serve HTML
            if self.path == '/' or self.path == '/index.html':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.encode())
            else:
                super().do_GET()

def run_server(veai_firmware, port=8000):
    """Run the VEAI web server"""
    handler = lambda *args, **kwargs: VEAHandler(*args, veai_firmware=veai_firmware, **kwargs)
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"VEAI Control UI running at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("Starting VEAI Web UI...")
    run_server(None)
