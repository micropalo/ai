import subprocess
import os
import sys
import speech_recognition as sr
import ollama
from faster_whisper import WhisperModel

# --- CONFIGURATION ---
PIPER_EXEC = "/usr/bin/piper-tts"
VOICE_MODEL = "en_US-lessac-medium.onnx"
LLM_MODEL = "llama3.2:1b"

# Load Whisper Offline Model (Using 'tiny' for i3 CPU speed)
# 'int8' quantization makes it use less RAM/CPU
print("Loading Offline Ears...")
whisper = WhisperModel("tiny", device="cpu", compute_type="int8")

recognizer = sr.Recognizer()

def speak(text):
    """The Mouth (Local Piper)"""
    clean_text = text.replace("*", "").replace("#", "")
    padded_text = f" . . {clean_text}"
    command = (
        f'echo "{padded_text}" | '
        f'{PIPER_EXEC} --model {VOICE_MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    subprocess.run(command, shell=True, check=True)

def listen_offline():
    """The Ears (Local Faster-Whisper)"""
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
        
        # Save audio to a temp file for Whisper
        with open("temp_speech.wav", "wb") as f:
            f.write(audio.get_wav_data())

    # Transcribe the file locally
    segments, _ = whisper.transcribe("temp_speech.wav", beam_size=1)
    text = "".join([segment.text for segment in segments]).strip()
    return text if text else None

def main():
    print(f"--- 100% OFFLINE AI READY ---")
    speak("System is now fully offline and ready.")

    while True:
        user_input = listen_offline()
        
        if user_input:
            print(f"You: {user_input}")
            
            # Brain (Ollama)
            response = ollama.chat(model=LLM_MODEL, messages=[
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
