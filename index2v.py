import subprocess
import os
import sys
import speech_recognition as sr
import ollama
from faster_whisper import WhisperModel

# --- CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts"
VOICE_MODEL = "en_US-lessac-medium.onnx"
LLM_MODEL = "llama3.2:1b"

# Load Whisper (CPU Optimized)
whisper = WhisperModel("tiny", device="cpu", compute_type="int8")
recognizer = sr.Recognizer()

def speak(text):
    """The Mouth: Blunt & Fast"""
    # Remove all formatting for faster TTS
    clean_text = text.replace("*", "").replace("#", "").strip()
    if not clean_text: return
    
    command = (
        f'echo ". {clean_text}" | '
        f'{PIPER_EXEC} --model {VOICE_MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    subprocess.run(command, shell=True, check=True)

def listen_offline():
    """The Ears: Filtered for Accuracy"""
    with sr.Microphone() as source:
        print("\n[Listening...]")
        # Set a high threshold to ignore background noise/breathing
        recognizer.energy_threshold = 600 
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            with open("temp.wav", "wb") as f: f.write(audio.get_wav_data())

            segments, _ = whisper.transcribe("temp.wav", beam_size=1)
            text = "".join([s.text for s in segments]).strip().lower()
            
            # Ignore hallucinations (Whisper likes to 'hear' static as 'Thank you')
            if len(text) < 3 or text in ["thank you.", "thanks for watching.", "you"]:
                return None
            return text
        except:
            return None

def main():
    print("--- BLUNT OFFLINE AI ---")
    
    while True:
        user_input = listen_offline()
        if user_input:
            print(f"You: {user_input}")
            
            # THE BRAIN: Forced to be blunt via System Message
            response = ollama.chat(model=LLM_MODEL, messages=[
                {'role': 'system', 'content': 'Be blunt, brief, and technical. No fluff. Max 2 sentences.'},
                {'role': 'user', 'content': user_input},
            ])
            
            ai_reply = response['message']['content']
            print(f"AI: {ai_reply}")
            speak(ai_reply)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
