import os
import sys
import io
import speech_recognition as sr
from faster_whisper import WhisperModel

# 1. NVIDIA DLL PATH FIX
# Explicitly pointing to the CUDA/cuDNN folders in your chiron_env
os.environ["PATH"] += os.pathsep + r'C:\Users\Nishaad\chiron_env\Lib\site-packages\nvidia\cublas\bin'
os.environ["PATH"] += os.pathsep + r'C:\Users\Nishaad\chiron_env\Lib\site-packages\nvidia\cudnn\bin'

# 2. MODEL INITIALIZATION
# Using 'medium.en' for high precision. 
# 'cuda' utilizes your RTX 3050, 'float16' optimizes VRAM usage.
print("Loading Chiron's hearing module (Medium Model)...")
model = WhisperModel("medium.en", device="cuda", compute_type="float16")

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    
    # Tuning for background noise (common in dorms/laptops)
    recognizer.energy_threshold = 300 
    recognizer.dynamic_energy_threshold = True
    
    mic = sr.Microphone()

    with mic as source:
        print("\n[Chiron is listening...]")
        # Calibrates for room hum before listening
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        
        try:
            # phrase_time_limit prevents it from waiting forever if it hears noise
            audio = recognizer.listen(source, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None

    try:
        print("[Processing...]")
        audio_data = io.BytesIO(audio.get_wav_data())
        
        # 3. TRANSCRIPTION ENGINE
        # beam_size=10: AI explores more word possibilities for better context
        # vad_filter: Blocks non-speech sounds (keyboard clicks, fans)
        segments, info = model.transcribe(
            audio_data, 
            beam_size=10, 
            vad_filter=True, 
            vad_parameters=dict(min_silence_duration_ms=700, min_speech_duration_ms=250)
        )
        
        text = "".join([segment.text for segment in segments])
        return text.strip()

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Module Ready. You can start speaking.")
    while True:
        result = listen_and_transcribe()
        if result:
            print(f"You said: {result}")
        elif result == "":
            print("[No speech detected]")