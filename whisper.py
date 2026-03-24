from faster_whisper import WhisperModel
import time

# 'tiny.en' uses ~200MB RAM. 'base.en' uses ~400MB.
model_size = "tiny.en"

print(f"Loading Whisper {model_size}...")
# On your i3 PC, use compute_type="float16" if you have a GPU, 
# but for CPU-only (and OPi One), use "int8"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def test_whisper():
    print("Whisper is ready. Waiting for audio file...")
    # Whisper works best by transcribing an actual file
    start = time.time()
    
    # We will point this to the response.mp3 or a recorded wav later
    segments, info = model.transcribe("test_audio.wav", beam_size=5)

    for segment in segments:
        print(f"[Detected: {info.language}] user input: {segment.text}")
        if "exit" in segment.text.lower():
            print("user said exit user will exit")
            return

    print(f"Done in {time.time() - start:.2f}s")

if __name__ == "__main__":
    # You'll need to record a quick 'test_audio.wav' to run this test
    test_whisper()
 
