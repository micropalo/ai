import subprocess
import sys

def speak_offline(text):
    """
    Uses espeak-ng to talk immediately without internet.
    -s 160: Speed (words per minute). 160-175 is usually natural.
    -p 40:  Pitch. Lower numbers sound deeper/more robotic.
    -v en-us: Voice variant (English US).
    """
    print(f"Computer says: {text}")
    
    try:
        # We use subprocess to call the system command directly
        subprocess.run([
            "espeak-ng", 
            "-s", "165", 
            "-p", "45", 
            "-v", "en-us", 
            text
        ], check=True)
    except FileNotFoundError:
        print("Error: espeak-ng is not installed. Run 'sudo pacman -S espeak-ng'")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("--- OFFLINE ESPEAK-NG TESTER ---")
    print("Type something and press Enter (type 'exit' to quit)")
    
    while True:
        try:
            user_input = input("\n> ")
            
            if user_input.lower() == 'exit':
                print("Closing speaker test...")
                break
                
            if user_input.strip():
                speak_offline(user_input)
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
