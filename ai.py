import ollama
import stt
import tts
import sys

LLM_MODEL = "llama3.2:1b"

def main():
    print(f"--- MODULAR OFFLINE AI (Arch Linux) ---")
    tts.speak("Systems initialized. Modules online.")

    while True:
        # 1. Get text from STT module
        user_input = stt.listen()
        
        if user_input and len(user_input) > 2:
            print(f"You: {user_input}")
            
            # 2. Process with Ollama
            try:
                response = ollama.chat(model=LLM_MODEL, messages=[
                    {'role': 'system', 'content': 'Be blunt and technical. 2 sentences max.'},
                    {'role': 'user', 'content': user_input},
                ])
                reply = response['message']['content']
                print(f"AI: {reply}")
                
                # 3. Send to TTS module
                tts.speak(reply)
            except Exception as e:
                print(f"Ollama Error: {e}")
        else:
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutting down modules...")
        sys.exit(0)
