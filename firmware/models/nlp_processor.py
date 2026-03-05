#!/usr/bin/env python3
"""
VEAI NLP Processor
AI Brain - Natural Language Processing and Chat

Models:
- HuggingFace Transformers - LLM for conversation
- Sentence Transformers - Semantic similarity
- Rule-based responses - Fallback
"""

import os
import time
import random

class NLPProcessor:
    """AI Brain - Natural Language Processing"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.use_llm = False
        self.conversation_history = []
        
        # Rule-based responses (fallback)
        self.responses = {
            "greeting": [
                "Hello! I'm VEAI. How can I help you?",
                "Hi there! What can I do for you?",
                "Hey! I'm here to assist you."
            ],
            "who": [
                "I'm VEAI - Voice, Eyes, and Ears Artificial Intelligence.",
                "I'm an AI assistant running on Raspberry Pi with ESP32.",
                "I'm your AI companion with vision, hearing, and voice capabilities."
            ],
            "capabilities": [
                "I can see using the camera, hear using microphones, and speak using text-to-speech.",
                "My features include object detection, face recognition, speech recognition, and voice output.",
                "I have AI eyes for vision, AI ears for hearing, and AI voice for speaking."
            ],
            "sensors": [
                "I have a PIR motion sensor, HC-SR04 distance sensor, and DHT22 temperature/humidity sensor.",
                "My sensors detect motion, measure distance, and read environmental conditions."
            ],
            "default": [
                "I'm not sure I understand. Can you try again?",
                "Could you rephrase that?",
                "I didn't catch that. Try asking about my capabilities!"
            ]
        }
        
    def init_transformers(self):
        """Initialize HuggingFace Transformers for LLM"""
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            # Use small model for Raspberry Pi
            model_name = "microsoft/phi-1_5"  # ~1GB, good for Pi 4
            
            print(f"Loading {model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            self.use_llm = True
            print(f"LLM loaded: {model_name}")
            return True
        except Exception as e:
            print(f"Transformers init failed: {e}")
            print("Using rule-based responses instead")
            return False
            
    def init_sentence_transformers(self):
        """Initialize Sentence Transformers for semantic similarity"""
        try:
            from sentence_transformers import SentenceTransformer
            
            # Use small model
            self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
            print("Sentence Transformers loaded")
            return True
        except Exception as e:
            print(f"Sentence Transformers init failed: {e}")
            return False
            
    def generate_response_llm(self, prompt):
        """Generate response using LLM"""
        if not self.use_llm or not self.model:
            return None
            
        try:
            # Add conversation context
            full_prompt = "\n".join(self.conversation_history[-5:])
            full_prompt += f"\nHuman: {prompt}\nAI:"
            
            # Generate
            inputs = self.tokenizer(full_prompt, return_tensors="pt")
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,
                temperature=0.7,
                do_sample=True
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            response = response.split("AI:")[-1].strip()
            
            return response
            
        except Exception as e:
            print(f"LLM generation failed: {e}")
            return None
            
    def generate_response_rulebased(self, text):
        """Generate response using rule-based system"""
        text_lower = text.lower()
        
        # Check for keywords
        if any(w in text_lower for w in ["hello", "hi", "hey", "greetings"]):
            return random.choice(self.responses["greeting"])
            
        if any(w in text_lower for w in ["who", "what are you", "your name"]):
            return random.choice(self.responses["who"])
            
        if any(w in text_lower for w in ["what can you do", "capabilities", "features", "abilities"]):
            return random.choice(self.responses["capabilities"])
            
        if any(w in text_lower for w in ["sensor", "pir", "distance", "temperature", "dht"]):
            return random.choice(self.responses["sensors"])
            
        # Check for questions
        if "?" in text:
            if any(w in text_lower for w in ["see", "vision", "camera"]):
                return "Yes! I have AI eyes using the Pi Camera. I can detect objects, faces, and more!"
            if any(w in text_lower for w in ["hear", "listen", "microphone"]):
                return "Yes! I have AI ears using the INMP441 microphone. I can recognize speech!"
            if any(w in text_lower for w in ["speak", "talk", "voice", "say"]):
                return "Yes! I have AI voice using the PAM8403 amplifier and speaker. I can talk back!"
                
        return random.choice(self.responses["default"])
        
    def process(self, text):
        """Process input text and generate response"""
        # Add to history
        self.conversation_history.append(f"Human: {text}")
        
        # Try LLM first
        if self.use_llm:
            response = self.generate_response_llm(text)
            if response:
                self.conversation_history.append(f"AI: {response}")
                return response
                
        # Fallback to rule-based
        response = self.generate_response_rulebased(text)
        self.conversation_history.append(f"AI: {response}")
        
        # Keep history manageable
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
            
        return response
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        
    def get_context(self):
        """Get conversation summary"""
        return "\n".join(self.conversation_history[-5:])


class CommandProcessor:
    """Process commands from text input"""
    
    def __init__(self, veai_controller=None):
        self.veai = veai_controller
        self.commands = {
            "look": self.cmd_look,
            "listen": self.cmd_listen,
            "say": self.cmd_say,
            "status": self.cmd_status,
            "sensors": self.cmd_sensors,
            "help": self.cmd_help
        }
        
    def process(self, text):
        """Process command from text"""
        text_lower = text.lower().strip()
        
        # Check for known commands
        for cmd, func in self.commands.items():
            if text_lower.startswith(cmd):
                return func(text_lower)
                
        return None
        
    def cmd_look(self, text):
        """Take a look / capture image"""
        if self.veai:
            result = self.veai.process_vision()
            if result:
                return f"I can see! Image captured at {result['width']}x{result['height']}"
        return "Looking around..."
        
    def cmd_listen(self, text):
        """Listen for voice input"""
        return "Listening..."
        
    def cmd_say(self, text):
        """Speak text after 'say'"""
        # Extract text to say
        text_to_say = text.replace("say", "").strip()
        if text_to_say and self.veai:
            # This would trigger TTS
            return f"Speaking: {text_to_say}"
        return "What should I say?"
        
    def cmd_status(self, text):
        """Get system status"""
        if self.veai:
            status = self.veai.get_status()
            return f"State: {status['state']}, Camera: {status['camera']}, Sensors: Active"
        return "System operational"
        
    def cmd_sensors(self, text):
        """Get sensor data"""
        if self.veai:
            s = self.veai.sensor_data
            return f"Motion: {s.motion}, Distance: {s.distance:.1f}cm, Temp: {s.temperature:.1f}C, Humidity: {s.humidity:.1f}%"
        return "Sensors offline"
        
    def cmd_help(self, text):
        """Show help"""
        return """Available commands:
- look: Capture and process image
- listen: Activate voice recognition
- say [text]: Speak the text
- status: Show system status
- sensors: Show sensor readings
- help: Show this help"""


# Demo
if __name__ == "__main__":
    print("VEAI NLP Processor Test")
    print("-" * 30)
    
    nlp = NLPProcessor()
    
    # Try to initialize LLM
    nlp.init_transformers()
    
    # Test conversations
    print("\nTesting conversation:")
    
    test_inputs = [
        "Hello!",
        "Who are you?",
        "What can you do?",
        "What do you see?"
    ]
    
    for text in test_inputs:
        response = nlp.process(text)
        print(f"You: {text}")
        print(f"VEAI: {response}")
        print()
