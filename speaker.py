import subprocess
import os
import threading
import time

# --- CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts"
# Ensure this path is correct for your system
MODEL = "en_US-lessac-medium.onnx"

def keep_speaker_awake():
    """
    Background worker: Creates a continuous stream of digital silence.
    This prevents Bluetooth devices from entering power-save mode.
    """
    print("[BT] Starting continuous silence stream...")
    try:
        # We read from /dev/zero and pipe it to aplay infinitely.
        # This creates a 'warm' connection that never disconnects.
        subprocess.run(
            ["aplay", "-r", "22050", "-c", "1", "-f", "S16_LE", "/dev/zero"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print(f"[BT] Heartbeat stopped: {e}")

# 1. Start the 'Infinite Silence' thread
# It will run in the background as long as the script is open.
bt_heartbeat = threading.Thread(target=keep_speaker_awake, daemon=True)
bt_heartbeat.start()

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found!")
        return

    print(f"Llama says: {text}")
    
    # We use a slightly different command to ensure it mixes with the background silence
    # Note: If you get a 'Device or resource busy' error, 
    # make sure you are using PulseAudio or PipeWire (default on most modern Linux).
    command = (
        f'echo "{text}" | '
        f'{PIPER_EXEC} --model {MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Audio Error: {e}")

def main():
    print("--- PIPER SPEAKER (BLUETOOTH ALWAYS-ON) ---")
    print("Sending 0Hz 'Digital Silence' to keep device awake.")
    
    # Wait 2 seconds to let the Bluetooth handshaking finish
    time.sleep(2)
    
    while True:
        try:
            user_input = input("\nType to speak (or 'exit'): ")
            
            if user_input.lower() == 'exit':
                break
                
            if user_input.strip():
                speak_piper(user_input)
                
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
