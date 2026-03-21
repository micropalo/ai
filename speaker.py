import subprocess

def speak_offline(text):
    print(f"Llama: {text}")
    # Using 'pipewire' as the device automatically routes to your Bluetooth
    cmd = f"espeak-ng -v en-us -s 160 '{text}' --stdout | aplay -D pipewire"
    subprocess.run(cmd, shell=True)
 
