import subprocess
import os
import threading
import time

# --- HARDWARE CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts"
MODEL = "en_US-lessac-medium.onnx"
# TARGET: HDMI Hardware Address (Card 1, Device 7)
HDMI_DEVICE = "hw:1,7"

def keep_speaker_awake():
    """
    Background worker: Keeps the HDMI 'pipe' open.
    Even though HDMI doesn't sleep like BT, keeping the stream 
    initially active prevents 'popping' sounds.
    """
    while True:
        try:
            # Pinging HDMI Device 1,7
            subprocess.run(
                ["aplay", "-D", HDMI_DEVICE, "-d", "1", "-r", "22050", "-f", "S16_LE", "/dev/zero"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(10) # HDMI is more stable, so we can wait longer
        except:
            break

# Start the 'Heartbeat' thread
bt_heartbeat = threading.Thread(target=keep_speaker_awake, daemon=True)
bt_heartbeat.start()

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found in {os.getcwd()}")
        return

    print(f"HDMI Output: {text}")
    
    # We use -D {HDMI_DEVICE} to force the audio to your monitor
    command = (
        f'echo "{text}" | '
        f'{PIPER_EXEC} --model {MODEL} --output-raw | '
        f'aplay -D {HDMI_DEVICE} -r 22050 -f S16_LE -t raw'
    )
    
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"\n[!] Hardware Error: Is HDMI 1,7 correct?")
        print(f"Check with: aplay -l")
        print(f"Error details: {e}")

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
