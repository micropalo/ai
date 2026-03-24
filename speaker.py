import subprocess
import os
import time

# --- HARDWARE CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts" 
MODEL = "en_US-lessac-medium.onnx"

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found!")
        return

    print(f"Assistant: {text}")

    try:
        # STEP 1: Wake up the Bluetooth Speaker
        # We play 2 seconds of silence using '/dev/zero'
        # -d 2: duration 2 seconds
        # -r 22050: matches Piper's rate to keep the hardware synced
        print("Waking up speaker...")
        subprocess.run(
            ["aplay", "-d", "2", "-r", "22050", "-f", "S16_LE", "/dev/zero"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # STEP 2: Speak the text
        # We use a slight delay (0.1s) after the silence for stability
        time.sleep(0.1)
        
        command = (
            f'echo "{text}" | '
            f'{PIPER_EXEC} --model {MODEL} --output-raw | '
            f'aplay -r 22050 -f S16_LE -t raw'
        )
        
        subprocess.run(command, shell=True, check=True)

    except Exception as e:
        print(f"Hardware/Audio Error: {e}")

def main():
    print("--- NEURAL SPEAKER (2s BT WAKE-UP) ---")
    print("Testing on TG-116 Bluetooth Speaker")
    
    while True:
        try:
            user_input = input("\nEnter text: ")
            if user_input.lower() == 'exit':
                break
            if user_input.strip():
                speak_piper(user_input)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
