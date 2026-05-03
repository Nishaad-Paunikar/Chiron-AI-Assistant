import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) # Usually the male 'Jarvis-style' voice
    engine.setProperty('rate', 175)
    print(f"Chiron: {text}")
    engine.say(text)
    engine.runAndWait()