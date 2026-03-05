#!/usr/bin/env python3
"""
VEAI Voice Processor
AI Ears - Speech Recognition and Text-to-Speech

Uses pre-trained models:
- Whisper (OpenAI) - speech to text
- Vosk - lightweight offline recognition
- pyttsx3 / Coqui - text to speech
"""

import os
import sys
import time
import threading
import numpy as np

class VoiceProcessor:
    """AI Ears - Voice input/output processing"""
    
    def __init__(self):
        self.recognizer = None
        self.tts_engine = None
        self.is_listening = False
        self.last_text = ""
        self.confidence = 0.0
        
    def init_whisper(self):
        """Initialize Whisper for speech recognition"""
        try:
            import whisper
            self.recognizer = whisper.load_model("tiny")
            print("Whisper loaded (tiny model)")
            return True
        except Exception as e:
            print(f"Whisper init failed: {e}")
            return False
            
    def init_vosk(self):
        """Initialize Vosk for offline speech recognition"""
        try:
            from vosk import Model, KaldiRecognizer
            model_path = os.path.join(os.path.dirname(__file__), "voice", "vosk-model-small")
            if os.path.exists(model_path):
                self.vosk_model = Model(model_path)
                self.recognizer = KaldiRecognizer(self.vosk_model, 16000)
                print("Vosk loaded")
                return True
            else:
                print("Vosk model not found - run install_models.py")
                return False
        except Exception as e:
            print(f"Vosk init failed: {e}")
            return False
            
    def init_tts(self):
        """Initialize text-to-speech"""
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            print("TTS (pyttsx3) initialized")
            return True
        except Exception as e:
            print(f"TTS init failed: {e}")
            return False
            
    def listen_whisper(self, audio_data):
        """Recognize speech using Whisper"""
        if not self.recognizer:
            return None
            
        try:
            result = self.recognizer.transcribe(audio_data)
            self.last_text = result.get("text", "")
            self.confidence = result.get("confidence", 0.0)
            return self.last_text
        except Exception as e:
            print(f"Whisper recognition failed: {e}")
            return None
            
    def listen_vosk(self, audio_data):
        """Recognize speech using Vosk"""
        if not hasattr(self, 'recognizer'):
            return None
            
        try:
            if self.recognizer.AcceptWaveform(audio_data):
                result = eval(self.recognizer.Result())
                self.last_text = result.get("text", "")
                return self.last_text
        except Exception as e:
            print(f"Vosk recognition failed: {e}")
            return None
            
    def speak(self, text):
        """Convert text to speech"""
        if not self.tts_engine:
            print("TTS not initialized")
            return
            
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS failed: {e}")
            
    def speak_async(self, text):
        """Speak in background thread"""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
        
    def get_audio_from_mic(self, duration=3):
        """Get audio from microphone (placeholder)"""
        # In real implementation, this would capture from I2S mic
        # through ESP32 serial or directly connected USB mic
        print(f"Recording {duration} seconds...")
        # Return numpy array of audio samples
        return np.zeros(16000 * duration)


class VoiceRecognition:
    """Pre-configured voice recognition pipeline"""
    
    def __init__(self, model="whisper"):
        self.processor = VoiceProcessor()
        self.model_type = model
        
        # Initialize based on preference
        if model == "whisper":
            self.processor.init_whisper()
        elif model == "vosk":
            self.processor.init_vosk()
            
        self.processor.init_tts()
        
    def listen(self, timeout=5):
        """Listen and recognize speech"""
        print("Listening...")
        audio = self.processor.get_audio_from_mic(timeout)
        
        if self.model_type == "whisper":
            text = self.processor.listen_whisper(audio)
        else:
            text = self.processor.listen_vosk(audio)
            
        print(f"Recognized: {text}")
        return text
        
    def respond(self, text):
        """Speak the response"""
        self.processor.speak_async(text)
        return True


# Demo
if __name__ == "__main__":
    print("VEAI Voice Processor Test")
    print("-" * 30)
    
    # Try to initialize
    voice = VoiceRecognition("whisper")
    
    # Test TTS
    print("\nTesting TTS...")
    voice.respond("Hello! I am VEAI, your AI assistant.")
    
    print("\nReady for voice input!")
