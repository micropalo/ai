import speech_recognition as sr
import ollama
from gtts import gTTS
import subprocess
import os

# Initialize the 'Ears'
r = sr.Recognizer()

def speak(text):
    print(f"Llama: {text}")
    filename = "response.mp3"
    
    # Convert text to speech file
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    
    # Force playback to specific HDMI card (1,7) using mpv
    # plughw is used to handle sample rate conversions automatically
    cmd = ["mpv", "--audio-device=alsa/plughw:1,7", "--no-video", filename]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Optional: Clean up the file after playing to keep the folder tidy
    if os.path.exists(filename):
        os.remove(filename)

def main():
    while True:
        with sr.Microphone() as source:
            print("\n[LISTENING] Ask Llama a question...")
            # Adjust for ambient noise to improve recognition accuracy
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # Listen for input
                audio = r.listen(source, timeout=10)
                user_text = r.recognize_google(audio)
                print(f"You: {user_text}")
                
                # Send to Llama 3.2 1B via Ollama
                response = ollama.chat(model='llama3.2:1b', messages=[
                    {
                        'role': 'system', 
                        'content': 'Answer only in 10 words or less. Be very blunt.'
                    },
                    {
                        'role': 'user', 
                        'content': user_text
                    },
                ])

                # Extract the reply and trigger the speakers
                reply = response['message']['content']
                speak(reply)
                
            except sr.UnknownValueError:
                # Speech was unintelligible
                continue
            except sr.RequestError:
                print("Could not request results from Google Speech Recognition service")
                continue
            except Exception as e:
                # Catch-all for other issues (like Ollama being offline)
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    main()
