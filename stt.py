import speech_recognition as sr
from faster_whisper import WhisperModel
import os

# Use 'small' for niche word accuracy on your i3
model = WhisperModel("small", device="cpu", compute_type="int8")
recognizer = sr.Recognizer()

def load_words():
    if os.path.exists("words.txt"):
        with open("words.txt", "r") as f:
            return f.read().strip()
    return ""

def listen():
    with sr.Microphone() as source:
        recognizer.energy_threshold = 600
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            with open("temp.wav", "wb") as f: f.write(audio.get_wav_data())
            
            segments, _ = model.transcribe(
                "temp.wav", 
                beam_size=5, 
                initial_prompt=load_words(),
                vad_filter=True
            )
            return "".join([s.text for s in segments]).strip()
        except:
            return None
