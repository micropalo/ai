import os
import sys
import json
import queue
import vosk
import sounddevice as sd
import ollama

# 1. SETUP PATHS
# Make sure this matches your unzipped folder name in Arch
MODEL_PATH = "model-en" 

if not os.path.exists(MODEL_PATH):
    print(f"ERROR: Model folder '{MODEL_PATH}' not found!")
    sys.exit(1)

# 2. INITIALIZE VOSK & AUDIO QUEUE
model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    """Callback for the sounddevice input stream"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def speak_offline(text):
    """Uses espeak-ng to talk through your Bluetooth speaker"""
    print(f"Llama: {text}")
    # We use 'aplay -D pipewire' to send audio to your Bluetooth default
    cmd = f"espeak-ng -v en-us -s 160 '{text}' --stdout | aplay -D pipewire"
    os.system(cmd)

def main():
    # Start listening to your USB Mic (16000Hz is standard for Vosk)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        
        print(f"\n[LOCAL AI READY] Using model: {MODEL_PATH}")
        print("Talk to Llama now... (Ctrl+C to stop)")
        
        rec = vosk.KaldiRecognizer(model, 16000)
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                user_text = result.get("text", "")
                
                if user_text.strip():
                    print(f"You: {user_text}")
                    
                    # Send to Local Llama 3.2 1B
                    response = ollama.chat(model='llama3.2:1b', messages=[
                        {'role': 'user', 'content': user_text},
                    ])
                    
                    reply = response['message']['content']
                    speak_offline(reply)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping AI...")
