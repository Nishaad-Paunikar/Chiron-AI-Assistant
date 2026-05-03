from stt_handler import listen_and_transcribe
from brain import parse_intent
from actions import ACTION_MAP
from voice_engine import speak

def main():
    speak("Chiron systems online. How can I help, Nishaad?")
    
    running = True
    while running:
        user_speech = listen_and_transcribe()
        
        if user_speech:
            decision = parse_intent(user_speech)
            
            if "ACTION:SHUTDOWN" in decision:
                speak("Understood. Powering down systems. Goodbye, Nishaad.")
                running = False # This breaks the loop
                
            elif "ACTION:" in decision:
                # ... your existing action handling code ...
                action_part = decision.replace("ACTION:", "").strip().split("|")
                cmd = action_part[0]
                arg = action_part[1] if len(action_part) > 1 else "local"
                
                if cmd in ACTION_MAP:
                    result = ACTION_MAP[cmd](arg)
                    speak(result)
            else:
                speak(decision)

if __name__ == "__main__":
    main()