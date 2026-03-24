import subprocess
import os

# --- HARDWARE CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts" 
MODEL = "en_US-lessac-medium.onnx"

# CHANGED: Using 'plughw' instead of 'hw' to avoid "Device Busy" errors
HDMI_DEVICE = "plughw:2,7"

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found!")
        return

    # TECHNICAL FIX: Added ' . . ' to the start of the string.
    # This gives the HDMI receiver a split second to 'wake up' 
    # and prevents the first letter of your word from being cut off.
    padded_text = f" . . {text}"

    print(f"HDMI Output ({HDMI_DEVICE}): {text}")

    command = (
        f'echo "{padded_text}" | '
        f'{PIPER_EXEC} --model {MODEL} --output-raw | '
        f'aplay -D {HDMI_DEVICE} -r 22050 -f S16_LE -t raw'
    )

    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"\n[!] Audio Error: {e}")
        print("Check if Card 2, Device 7 is still the correct HDMI output.")

def main():
    print(f"--- PIPER SPEAKER (HDMI: {HDMI_DEVICE}) ---")
    print("Direct hardware routing active. Type 'exit' to quit.")
    
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
