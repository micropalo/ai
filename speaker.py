import subprocess
import os
import sys

# --- HARDWARE CONFIG ---
# Verified path from your 'whereis' command
PIPER_EXEC = "/usr/bin/piper-tts" 
# Ensure this is in /home/micro/ai/
MODEL = "en_US-lessac-medium.onnx"

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found in the current directory!")
        return

    # TECHNICAL FIX: We add a short pause at the start to wake up the 
    # TG-116 Bluetooth speaker before the first word is spoken.
    # We also use --sentence-silence to keep the speaker 'alive' between sentences.
    
    print(f"Assistant: {text}")

    # The 'lead-in' dots (...) help Piper generate a tiny bit of initial silence
    padded_text = f". . . {text}"

    command = (
        f'echo "{padded_text}" | '
        f'{PIPER_EXEC} --model {MODEL} --sentence-silence 0.5 --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )

    try:
        # Running via shell=True to handle the pipes (|)
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Hardware/Audio Error: {e}")

def main():
    print("--- NEURAL SPEAKER TEST (OFFLINE) ---")
    print("Bluetooth: Ensure TG-116 is connected.")
    print("Type 'exit' to stop.")
    
    while True:
        try:
            user_input = input("\nEnter text: ")
            
            if user_input.lower() == 'exit':
                print("Shutting down speaker...")
                break
                
            if user_input.strip():
                speak_piper(user_input)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
