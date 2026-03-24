import subprocess
import os
import threading
import time

# --- CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts"
MODEL = "en_US-lessac-medium.onnx"

def keep_speaker_awake():
    """
    Background worker: Sends a silent signal every 5 seconds 
    to prevent the TG-116 from sleeping.
    """
    # Using /dev/zero to send 0.5s of 'digital silence' 
    # This acts like a 'ping' to the Bluetooth controller.
    while True:
        try:
            subprocess.run(
                ["aplay", "-d", "1", "-r", "22050", "-f", "S16_LE", "/dev/zero"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # Wait 5 seconds before pinging again
            time.sleep(5)
        except:
            break

# 1. Start the 'Heartbeat' thread before anything else
# 'daemon=True' means it will close automatically when you exit the script
bt_heartbeat = threading.Thread(target=keep_speaker_awake, daemon=True)
bt_heartbeat.start()

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found!")
        return

    print(f"Llama says: {text}")
    
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
    print("--- PIPER SPEAKER (ALWAYS-AWAKE MODE) ---")
    print("Bluetooth 'Heartbeat' is active. Type 'exit' to quit.")
    
    # Give the heartbeat a second to wake the speaker initially
    time.sleep(1)
    
    while True:
        try:
            user_input = input("\nType to speak: ")
            
            if user_input.lower() == 'exit':
                break
                
            if user_input.strip():
                speak_piper(user_input)
                
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
