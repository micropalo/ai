import subprocess
import sys
import os

# --- CONFIGURATION ---
# Ensure these files are in the same folder as this script
MODEL = "en_US-lessac-medium.onnx"

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: Model file {MODEL} not found!")
        return

    print(f"Piper is speaking: {text}")

    # We pipe the text into piper, which outputs raw audio to aplay
    # aplay -r 22050: Piper 'medium' models usually output at 22050Hz
    command = (
        f'echo "{text}" | '
        f'piper --model {MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )

    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Audio Error: {e}")

def main():
    print("--- NEURAL OFFLINE SPEAKER (PIPER) ---")
    print("Type your text and press Enter. (type 'exit' to quit)")
    
    while True:
        user_input = input("\n> ")
        
        if user_input.lower() == 'exit':
            break
            
        if user_input.strip():
            speak_piper(user_input)

if __name__ == "__main__":
    main()
