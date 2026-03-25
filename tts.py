import subprocess

PIPER_EXEC = "/usr/bin/piper-tts"
VOICE_MODEL = "en_US-lessac-medium.onnx"

def speak(text):
    if not text: return
    clean_text = text.replace("*", "").replace("#", "").strip()
    
    # The '. .' wakes up the HDMI audio sync
    command = (
        f'echo ". . {clean_text}" | '
        f'{PIPER_EXEC} --model {VOICE_MODEL} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Audio Error: {e}")
 
