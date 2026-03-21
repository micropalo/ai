import os
import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# --- CONFIGURATION ---
# Change this to your actual model folder name
MODEL_PATH = "model-en" 

if not os.path.exists(MODEL_PATH):
    print(f"Error: Model not found at {MODEL_PATH}")
    sys.exit(1)

# Initialize Vosk
model = Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    """This handles the raw audio from the microphone"""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def test_stt():
    # 16000Hz is the standard for most Vosk models
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        
        print(f"--- OFFLINE STT TEST READY ---")
        print(f"Model: {MODEL_PATH}")
        print("Speak into your mic now. (Ctrl+C to stop)")
        
        rec = KaldiRecognizer(model, 16000)
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # This triggers when it detects a pause (end of sentence)
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print(f"\n>> Final Output: {text}")
            else:
                # This shows the "live" guessing as you talk
                partial = json.loads(rec.PartialResult())
                partial_text = partial.get("partial", "")
                if partial_text:
                    # Clear line and print partial to stay on one line
                    sys.stdout.write(f"\rListening: {partial_text}...")
                    sys.stdout.flush()

if __name__ == "__main__":
    try:
        test_stt()
    except KeyboardInterrupt:
        print("\nTest stopped by user.")
