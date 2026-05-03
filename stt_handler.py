import os
import sys
import io
import speech_recognition as sr
from faster_whisper import WhisperModel

# 1. NVIDIA DLL PATH FIX
os.environ["PATH"] += os.pathsep + r'C:\Users\Nishaad\chiron_env\Lib\site-packages\nvidia\cublas\bin'
os.environ["PATH"] += os.pathsep + r'C:\Users\Nishaad\chiron_env\Lib\site-packages\nvidia\cudnn\bin'

# 2. EXPANDED NAME CORRECTION MAP
# Added the specific errors you encountered ("I run", "I don't", "And on")
NAME_CORRECTIONS = {
    "shiron": "Chiron",
    "kyron": "Chiron",
    "sharon": "Chiron",
    "i run": "Chiron",
    "i don't": "Chiron",
    "and on": "Chiron",
    "yeah i don't": "Chiron",
    "nisha": "Nishaad",
    "nishad": "Nishaad",
    "nishat": "Nishaad",
    "nishaadad" : "Nishaad",
    "Nishaadad" : "Nishaad"
}

print("Loading Chiron's hearing module (Medium Model)...")
model = WhisperModel("medium.en", device="cuda", compute_type="float16")

def clean_transcription(text):
    if not text:
        return ""
    
    # Check for multi-word phrases first (like "i don't")
    lowercase_text = text.lower().strip(".,!?")
    for wrong, right in NAME_CORRECTIONS.items():
        if wrong in lowercase_text:
            lowercase_text = lowercase_text.replace(wrong, right)
    
    return lowercase_text.capitalize()

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 400 # Slightly higher to ignore faint mouth sounds
    recognizer.dynamic_energy_threshold = True
    
    mic = sr.Microphone()

    with mic as source:
        print("\n[Chiron is listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=1.0) # Increased for better calibration
        
        try:
            audio = recognizer.listen(source, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return None

    try:
        print("[Processing...]")
        audio_data = io.BytesIO(audio.get_wav_data())
        
        segments, info = model.transcribe(
            audio_data, 
            beam_size=10, 
            vad_filter=True, 
            # We use an initial_prompt to "bias" the model toward your name
            initial_prompt="Chiron, Nishaad, VIT, Llama, coding, Python",
            vad_parameters=dict(min_silence_duration_ms=700)
        )
        
        raw_text = "".join([segment.text for segment in segments]).strip()
        
        # If Whisper returns something very short like "I don't", clean_transcription handles it
        return clean_transcription(raw_text)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Module Ready. Try saying: 'Hello Chiron, it's Nishaad.'")
    while True:
        result = listen_and_transcribe()
        if result and len(result) > 2: # Ignore accidental 1-2 letter blips
            print(f"Chiron heard: {result}")