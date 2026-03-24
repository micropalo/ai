import subprocess
import os
import time
import speech_recognition as sr

# --- CONFIGURATION ---
PIPER_EXEC = "/usr/bin/piper-tts"
MODEL = "en_US-lessac-medium.onnx"

# Initialize the Recognizer (The 'Ears')
recognizer = sr.Recognizer()
# Using the Mic hardware on your Arch PC
mic = sr.Microphone()

def speak(text):
    """The 'Mouth' (Piper)"""
    # Adding padding dots to prevent HDMI/Bluetooth clipping
    padded_text = f" . . {text}"
    
    command = (
        f'echo "{padded_text}" | '
        f'{PIPER_EXEC} --model {MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Audio Output Error: {e}")

def listen():
    """The 'Ears' (Whisper/STT)"""
    with mic as source:
        print("\n[Listening...] Speak now.")
        # Adjust for ambient noise in your room
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("[Processing...]")
        # This uses the Google STT engine by default for speed, 
        # but you can swap to local Whisper if you have it set up.
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        print("Network error (Google STT requires internet).")
        return None

def main():
    print("--- ARCH LINUX AI: PIPER + WHISPER LOOP ---")
    print("System: Ready. (Ctrl+C to stop)")
    
    # Initial greeting
    speak("System online. I am listening.")

    while True:
        user_text = listen()
        
        if user_text:
            print(f"You said: {user_text}")
            
            # THE LOOP: For now, it just repeats what you said.
            # Later, we will insert the Llama 3 logic here.
            response = f"You said {user_text}"
            
            speak(response)
        else:
            # If it didn't hear anything, it just loops back to listening
            continue

if __name__ == "__main__":
    main()
 
