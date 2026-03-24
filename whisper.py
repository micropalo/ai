import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel
import os

# CONFIG
MODEL_SIZE = "tiny.en"
FILE_NAME = "test_audio.wav"
FS = 16000  # Sample rate
DURATION = 5  # Seconds to record

print(f"Loading Whisper {MODEL_SIZE}...")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

def record_and_test():
    print(f"\n[RECORDING] Speak for {DURATION} seconds...")
    # Record audio from your mic
    myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    
    # Save to the file Whisper is looking for
    sf.write(FILE_NAME, myrecording, FS)
    print(f"File saved as {FILE_NAME}. Processing...")

    # Transcribe the file
    segments, info = model.transcribe(FILE_NAME, beam_size=5)

    print("\n--- RESULT ---")
    for segment in segments:
        print(f"user input: {segment.text.strip()}")
        
        if "exit" in segment.text.lower():
            print("user said exit user will exit")
            return

    # Cleanup the test file
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)

if __name__ == "__main__":
    try:
        record_and_test()
    except Exception as e:
        print(f"Error: {e}")
