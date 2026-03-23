import os
import sys
import json
import queue
import vosk
import sounddevice as sd

# --- CONFIGURATION ---
# Replace with the actual folder name of your GigaSpeech model
MODEL_PATH = "us-model" 

if not os.path.exists(MODEL_PATH):
    print(f"ERROR: Model folder '{MODEL_PATH}' not found.")
    sys.exit(1)

# Initialize Vosk
model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    """Callback for the sounddevice input stream"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    # 16000Hz is required for most Vosk models
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            
            print("\n--- OFFLINE STT TESTER ---")
            rec = vosk.KaldiRecognizer(model, 16000)
            
            # This follows your requested flow
            print("listening now...") 
            
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    user_input = result.get("text", "")
                    
                    if user_input.strip():
                        print(user_input) # Your "user input" placeholder
                        
                        # Check for the exit command
                        if "exit" in user_input.lower():
                            print("user said exit user will exit")
                            break
                else:
                    # Optional: print partials if you want to see it live
                    # partial = json.loads(rec.PartialResult())
                    # print(f"Processing: {partial.get('partial', '')}", end='\r')
                    pass

    except Exception as e:
        print(f"\n[Hardware Error]: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
