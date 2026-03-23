import speech_recognition as sr
import ollama
from gtts import gTTS
import subprocess
import os

# --- CONFIGURATION ---
# N is your calibration duration
N = 1.5 
r = sr.Recognizer()

def speak(text):
    """Saves response to MP3 and plays via Bluetooth default"""
    print(f"Llama: {text}")
    filename = "response.mp3"
    
    # Generate the speech file
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    
    # Play using mpv (uses system default Bluetooth automatically)
    # Redirecting output to DEVNULL keeps your terminal clean
    subprocess.run(["mpv", "--no-video", filename], 
                   stdout=subprocess.DEVNULL, 
                   stderr=subprocess.DEVNULL)
    
    # Clean up the file after playing to keep your folder tidy
    if os.path.exists(filename):
        os.remove(filename)

def main():
    # --- 1. SMART CALIBRATION AT START ---
    print("Scanning Room Noise...")
    with sr.Microphone() as source:
        # Quick check first
        r.adjust_for_ambient_noise(source, duration=0.2)
        
        if r.energy_threshold > 1000:
            print(f"Noisy room detected ({int(r.energy_threshold)}). Calibrating for {N}s...")
            r.adjust_for_ambient_noise(source, duration=N)
        else:
            print(f"Quiet room detected ({int(r.energy_threshold)}). Using fast start.")
            r.adjust_for_ambient_noise(source, duration=0.5)

    # --- 2. MAIN CONVERSATION LOOP ---
    while True:
        with sr.Microphone() as source:
            print("\n[LISTENING] Ask Llama a question...")
            
            # Use N for the loop calibration if you prefer it consistent
            r.adjust_for_ambient_noise(source, duration=0.1) 
            
            try:
                # Listen for voice input
                audio = r.listen(source, timeout=10)
                user_text = r.recognize_google(audio)
                print(f"You: {user_text}")

                # --- 3. SEND TO LLAMA WITH SYSTEM PROMPT ---
                # This ensures the 'Short & Blunt' personality you wanted
                response = ollama.chat(model='llama3.2:1b', messages=[
                    {
                        'role': 'system', 
                        'content': 'Answer only in 10 words or less. Be very blunt.'
                    },
                    {
                        'role': 'user', 
                        'content': user_text
                    }
                ])

                # Get the blunt reply
                reply = response['message']['content']
                
                # --- 4. OUTPUT TO BLUETOOTH ---
                speak(reply)

            except Exception:
                # If it doesn't hear anything or fails, it just resets the loop
                continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting AI Assistant...")
