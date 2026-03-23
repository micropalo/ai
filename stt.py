import os
import sys
import json
import queue
import vosk
import sounddevice as sd

# 1. SETUP MODEL PATH
# Ensure this folder name matches your GigaSpeech model folder
MODEL_PATH = "us-model"

if not os.path.exists(MODEL_PATH):
    print(f"ERROR: Model folder '{MODEL_PATH}' not found in current directory.")
    sys.exit(1)

# Initialize the model
model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    """This function puts audio data from the mic into a queue"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    # Setup microphone parameters (16000Hz is standard for Vosk)
    # Using 'sd.RawInputStream' is the most stable way on Arch/PipeWire
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            
            print(f"--- VOSK GIGASPEECH TEST READY ---")
            print("Say anything... (or say 'exit' to quit)")
            
            rec = vosk.KaldiRecognizer(model, 16000)
            
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    # Final result (full sentence)
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    
                    if text.strip():
                        print(f"User said: {text}")
                        
                        # --- EXIT PLACEHOLDER ---
                        if "exit" in text.lower():
                            print("!!! EXIT COMMAND DETECTED !!!")
                            # Add your placeholder logic here (e.g., break, cleanup, etc.)
                            break
                else:
                    # Partial results (optional: uncomment to see live updates)
                    # partial = json.loads(rec.PartialResult())
                    # print(f"Listening... {partial.get('partial', '')}", end='\r')
                    pass

    except Exception as e:
        print(f"Hardware Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping...")
