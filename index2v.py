import speech_recognition as sr
import ollama
from gtts import gTTS
import subprocess
import os

# Initialize the 'Ears'
r = sr.Recognizer()

def speak(text):
    print(f"Llama: {text}")
    # Convert text to speech file
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    
    # Force playback to your specific HDMI card (1,7)
    # Using 'r' before the string ensures 'plughw:1,7' is read literally
    cmd = ["mpv", f"--audio-device=alsa/plughw:1,7", "--no-video", "response.mp3"]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    while True:
        with sr.Microphone() as source:
            print("\n[LISTENING] Ask Llama a question...")
            # Automatically adjust for background noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=10)
                user_text = r.recognize_google(audio)
                print(f"You: {user_text}")
                
                # Send to Llama 3.2 1B
                response = ollama.chat(model='llama3.2:1b', messages=[
                    {'role': 'user', 'content': user_text},
                ])
                
                speak(response['message']['content'])
                
            except Exception:
                # If it doesn't hear you, it just resets the loop
                continue

if __name__ == "__main__":
    main()
