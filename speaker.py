import subprocess
import os
import sys

# --- HARDWARE CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts" 
MODEL = "en_US-lessac-medium.onnx"
# FIXED: Based on your 'aplay -l', your TV is Card 2, Device 7
HDMI_DEVICE = "hw:2,7"

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found!")
        return

    print(f"HDMI Output ({HDMI_DEVICE}): {text}")

    # No background thread needed for HDMI. 
    # Just direct routing to the hardware.
    command = (
        f'echo "{text}" | '
        f'{PIPER_EXEC} --model {MODEL} --output-raw | '
        f'aplay -D {HDMI_DEVICE} -r 22050 -f S16_LE -t raw'
    )

    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"\n[!] Audio Error: {e}")

def main():
    print(f"--- PIPER SPEAKER (HDMI: {HDMI_DEVICE}) ---")
    print("Type 'exit' to quit.")
    
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
