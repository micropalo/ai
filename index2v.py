import subprocess
import os
import speech_recognition as sr
import ollama  # Make sure to: pip install ollama

# --- CONFIGURATION ---
PIPER_EXEC = "/usr/bin/piper-tts"
MODEL_PATH = "en_US-lessac-medium.onnx"
LLM_MODEL = "llama3.2:1b"  # Your local Ollama model

# Initialize the 'Ears'
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """The 'Mouth' (Piper)"""
    # Clean the text (remove asterisks or weird characters Llama might output)
    clean_text = text.replace("*", "").replace("#", "")
    padded_text = f" . . {clean_text}"
    
    command = (
        f'echo "{padded_text}" | '
        f'{PIPER_EXEC} --model {MODEL_PATH} --output-raw | '
        f'aplay -r 22050 -f S16_LE -t raw'
    )
    
    try:
        subprocess.run(command, shell=True, check=True)
    except Exception as e:
        print(f"Audio Output Error: {e}")

def listen():
    """The 'Ears' (STT)"""
    with mic as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("[Processing Speech...]")
            text = recognizer.recognize_google(audio)
            return text
        except:
            return None

def chat_with_llama(user_input):
    """The 'Brain' (Ollama)"""
    print(f"Thinking about: {user_input}")
    try:
        response = ollama.chat(model=LLM_MODEL, messages=[
            {'role': 'user', 'content': user_input},
        ])
        return response['message']['content']
    except Exception as e:
        return f"Brain Error: {e}"

def main():
    print(f"--- AI ONLINE (Model: {LLM_MODEL}) ---")
    speak("System integrated. How can I help you today?")

    while True:
        user_text = listen()
        
        if user_text:
            print(f"You: {user_text}")
            
            # 1. Get response from Llama
            ai_response = chat_with_llama(user_text)
            print(f"AI: {ai_response}")
            
            # 2. Speak the response
            speak(ai_response)
        else:
            continue

if __name__ == "__main__":
    main()
