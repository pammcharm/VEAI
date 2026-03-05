#!/usr/bin/env python3
"""
VEAI Unified Model Loader
Loads all AI models (Voice, Vision, NLP) with one call
"""

import os
import sys

# Add models directory to path
MODELS_DIR = os.path.dirname(os.path.abspath(__file__))

class VEAI:
    """Unified VEAI AI System"""
    
    def __init__(self):
        self.voice = None
        self.vision = None
        self.nlp = None
        self.command_processor = None
        
        print("🤖 Initializing VEAI AI System...")
        
    def load_voice(self):
        """Load voice recognition and TTS"""
        try:
            sys.path.insert(0, MODELS_DIR)
            from voice_processor import VoiceProcessor
            self.voice = VoiceProcessor()
            print("  ✅ Voice AI loaded")
            return True
        except Exception as e:
            print(f"  ❌ Voice AI failed: {e}")
            return False
            
    def load_vision(self):
        """Load computer vision"""
        try:
            sys.path.insert(0, MODELS_DIR)
            from vision_processor import VisionProcessor
            self.vision = VisionProcessor()
            print("  ✅ Vision AI loaded")
            return True
        except Exception as e:
            print(f"  ❌ Vision AI failed: {e}")
            return False
            
    def load_nlp(self):
        """Load NLP/Chat AI"""
        try:
            sys.path.insert(0, MODELS_DIR)
            from nlp_processor import NLPProcessor, CommandProcessor
            self.nlp = NLPProcessor()
            self.command_processor = CommandProcessor()
            print("  ✅ NLP AI loaded")
            return True
        except Exception as e:
            print(f"  ❌ NLP AI failed: {e}")
            return False
            
    def load_all(self):
        """Load all AI models"""
        print("\n" + "=" * 40)
        print("Loading VEAI Pre-trained Models")
        print("=" * 40 + "\n")
        
        voice_ok = self.load_voice()
        vision_ok = self.load_vision()
        nlp_ok = self.load_nlp()
        
        print("\n" + "=" * 40)
        print("VEAI AI System Ready!")
        print("=" * 40)
        
        return voice_ok or vision_ok or nlp_ok
        
    def listen(self):
        """Listen for voice input"""
        if self.voice:
            return self.voice.listen()
        return None
        
    def speak(self, text):
        """Speak text"""
        if self.voice:
            self.voice.respond(text)
            
    def see(self, frame):
        """Process vision frame"""
        if self.vision:
            objects = self.vision.detect_objects(frame)
            faces = self.vision.detect_faces(frame)
            hands = self.vision.detect_hands(frame)
            return {"objects": objects, "faces": faces, "hands": hands}
        return None
        
    def think(self, text):
        """Process text and generate response"""
        if self.nlp:
            # First try commands
            if self.command_processor:
                cmd_response = self.command_processor.process(text)
                if cmd_response:
                    return cmd_response
            # Then try NLP
            return self.nlp.process(text)
        return None
        
    def run_interactive(self):
        """Run interactive chat loop"""
        print("\n🎤 VEAI Interactive Mode")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                text = input("You: ")
                if text.lower() == "quit":
                    break
                    
                # Process and respond
                response = self.think(text)
                print(f"VEAI: {response}")
                
            except KeyboardInterrupt:
                break
                
        print("\nGoodbye!")


def main():
    """Demo / Test VEAI Models"""
    print("=" * 50)
    print("VEAI Pre-trained Models Test")
    print("=" * 50)
    
    # Create VEAI instance
    veai = VEAI()
    
    # Load all models
    veai.load_all()
    
    # Test chat
    print("\n--- Testing NLP ---")
    response = veai.think("Hello!")
    print(f"Test: Hello! -> {response}")
    
    response = veai.think("What can you do?")
    print(f"Test: What can you do? -> {response}")
    
    # Interactive mode
    print("\nStarting interactive mode...")
    veai.run_interactive()


if __name__ == "__main__":
    main()
