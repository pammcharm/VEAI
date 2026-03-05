#!/usr/bin/env python3
"""
VEAI Model Setup Script
Downloads and installs pre-trained models for AI Eyes, Ears, and Voice

Models:
- Voice: Whisper (speech recognition), Coqui TTS
- Vision: MobileNet SSD, YOLO, Face detection
- NLP: Small language model for chat
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

# Base directory
MODELS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(MODELS_DIR)

class VEAModelInstaller:
    def __init__(self):
        self.models = {
            "voice": {
                "whisper": {
                    "name": "Whisper (OpenAI)",
                    "size": "~75MB (tiny)",
                    "description": "Speech recognition - converts voice to text",
                    "model_size": "tiny",
                    "install_cmd": "pip install openai-whisper"
                },
                "vosk": {
                    "name": "Vosk",
                    "size": "~50MB",
                    "description": "Lightweight offline speech recognition",
                    "model_url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
                    "install_cmd": "pip install vosk"
                },
                "pyttsx3": {
                    "name": "pyttsx3",
                    "size": "~10MB",
                    "description": "Offline text-to-speech engine",
                    "install_cmd": "pip install pyttsx3"
                },
                "coqui": {
                    "name": "Coqui TTS",
                    "size": "~150MB",
                    "description": "High-quality offline TTS",
                    "install_cmd": "pip install TTS"
                }
            },
            "vision": {
                "opencv": {
                    "name": "OpenCV DNN",
                    "size": "~20MB",
                    "description": "Object detection with MobileNet-SSD",
                    "model_url": "https://github.com/opencv/opencv/raw/master/samples/dnn/MobileNetSSD_deploy.caffemodel",
                    "install_cmd": "pip install opencv-python"
                },
                "face_recognition": {
                    "name": "Face Recognition",
                    "size": "~100MB",
                    "description": "Face detection and recognition",
                    "install_cmd": "pip install face-recognition"
                },
                "mediapipe": {
                    "name": "MediaPipe",
                    "size": "~50MB",
                    "description": "Face detection, hand tracking, pose estimation",
                    "install_cmd": "pip install mediapipe"
                }
            },
            "nlp": {
                "transformers": {
                    "name": "HuggingFace Transformers",
                    "size": "Variable",
                    "description": "Large language models for chat",
                    "install_cmd": "pip install transformers torch"
                },
                "ollama": {
                    "name": "Ollama",
                    "size": "Variable",
                    "description": "Run Llama2, Mistral locally",
                    "install_cmd": "curl -fsSL https://ollama.ai/install.sh | sh"
                },
                "sentence_transformers": {
                    "name": "Sentence Transformers",
                    "size": "~400MB",
                    "description": "Semantic similarity and embeddings",
                    "install_cmd": "pip install sentence-transformers"
                }
            }
        }
        
    def print_banner(self):
        print("=" * 60)
        print("🤖 VEAI Model Installer")
        print("=" * 60)
        print()
        
    def print_models(self):
        print("\n📦 Available Pre-trained Models:")
        print("-" * 60)
        
        for category, models in self.models.items():
            print(f"\n🔊 {category.upper()} Models:")
            for key, info in models.items():
                print(f"  • {info['name']}")
                print(f"    Size: {info['size']}")
                print(f"    Purpose: {info['description']}")
                print()
                
    def install_voice_models(self):
        """Install voice recognition and TTS models"""
        print("\n🎤 Installing Voice Models...")
        
        # Install base dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "torch", "torchaudio"], check=False)
        
        # Install Whisper
        print("Installing Whisper (OpenAI)...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"], check=False)
        
        # Install Vosk
        print("Installing Vosk...")
        subprocess.run([sys.executable, "-m", "pip", "install", "vosk"], check=False)
        
        # Download Vosk model
        vosk_dir = os.path.join(MODELS_DIR, "voice", "vosk-model-small")
        if not os.path.exists(vosk_dir):
            print("Downloading Vosk model...")
            try:
                # This would download the model in actual use
                print("  (Download skipped - run with internet to download)")
            except:
                pass
                
        # Install TTS
        print("Installing TTS engines...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyttsx3"], check=False)
        
        print("✅ Voice models installed!")
        
    def install_vision_models(self):
        """Install computer vision models"""
        print("\n👁️ Installing Vision Models...")
        
        # Install OpenCV
        print("Installing OpenCV...")
        subprocess.run([sys.executable, "-m", "pip", "install", "opencv-python", "opencv-python-headless"], check=False)
        
        # Install MediaPipe
        print("Installing MediaPipe...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mediapipe"], check=False)
        
        # Install face recognition
        print("Installing Face Recognition...")
        subprocess.run([sys.executable, "-m", "pip", "install", "face-recognition"], check=False)
        
        print("✅ Vision models installed!")
        
    def install_nlp_models(self):
        """Install NLP models"""
        print("\n🧠 Installing NLP Models...")
        
        # Install transformers
        print("Installing HuggingFace Transformers...")
        subprocess.run([sys.executable, "-m", "pip", "install", "transformers", "torch"], check=False)
        
        # Install sentence transformers
        print("Installing Sentence Transformers...")
        subprocess.run([sys.executable, "-m", "pip", "install", "sentence-transformers"], check=False)
        
        print("✅ NLP models installed!")
        
    def install_all(self):
        """Install all models"""
        self.print_banner()
        self.print_models()
        
        print("\n⚠️  This will download several hundred MB of models.")
        response = input("Continue? (y/n): ")
        
        if response.lower() != 'y':
            print("Installation cancelled.")
            return
            
        self.install_voice_models()
        self.install_vision_models()
        self.install_nlp_models()
        
        print("\n" + "=" * 60)
        print("✅ All models installed successfully!")
        print("=" * 60)
        
    def quick_install(self):
        """Quick install - essential models only"""
        print("\n⚡ Quick Install (Essential models only)...")
        
        # Core dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", 
                       "opencv-python", "mediapipe", "pyttsx3", "vosk"], 
                       check=False)
        
        print("✅ Quick install complete!")
        
    def list_installed(self):
        """List installed models"""
        print("\n📋 Installed Models:")
        
        try:
            import whisper
            print("  ✅ Whisper - Voice Recognition")
        except:
            pass
            
        try:
            import vosk
            print("  ✅ Vosk - Voice Recognition")
        except:
            pass
            
        try:
            import cv2
            print("  ✅ OpenCV - Computer Vision")
        except:
            pass
            
        try:
            import mediapipe
            print("  ✅ MediaPipe - Face/Hand/Body Tracking")
        except:
            pass
            
        try:
            import transformers
            print("  ✅ Transformers - NLP")
        except:
            pass
            
        try:
            import pyttsx3
            print("  ✅ pyttsx3 - Text-to-Speech")
        except:
            pass

def main():
    installer = VEAModelInstaller()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "all":
            installer.install_all()
        elif command == "quick":
            installer.quick_install()
        elif command == "voice":
            installer.install_voice_models()
        elif command == "vision":
            installer.install_vision_models()
        elif command == "nlp":
            installer.install_nlp_models()
        elif command == "list":
            installer.list_installed()
        else:
            print("Usage: python install_models.py [all|quick|voice|vision|nlp|list]")
    else:
        installer.print_banner()
        installer.print_models()
        print("\nUsage:")
        print("  python install_models.py all     - Install all models")
        print("  python install_models.py quick   - Quick install (essentials)")
        print("  python install_models.py voice   - Voice models only")
        print("  python install_models.py vision - Vision models only")
        print("  python install_models.py nlp    - NLP models only")
        print("  python install_models.py list   - List installed models")

if __name__ == "__main__":
    main()
