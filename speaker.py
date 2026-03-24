import subprocess
import os

# --- HARDWARE CONFIG ---
PIPER_EXEC = "/usr/bin/piper-tts" 
MODEL = "en_US-lessac-medium.onnx"

def speak_piper(text):
    if not os.path.exists(MODEL):
        print(f"Error: {MODEL} not found!")
        return

    # Adding dots to prevent the start of the word from being cut off
    padded_text = f" . . {text}"

    print(f"Speaking: {text}")

    # REMOVED: -D plughw:2,7
    # By removing the -D flag, aplay uses your DEFAULT system output.
    # Just make sure your TV/Monitor is selected in your system sound settings.
    command = (
        f'echo "{padded_text}" | '
        f'{PIPER_EXEC} --model {MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )

    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"\n[!] Audio Error: {e}")

def main():
    print("--- PIPER SPEAKER (SYSTEM DEFAULT) ---")
    print("Ensure your HDMI output is selected in your OS sound settings.")
    
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
