from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psutil
import GPUtil
import requests

# This imports the exact Whisper module you just shared
from stt_handler import listen_and_transcribe

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/system-vitals")
def get_vitals():
    gpus = GPUtil.getGPUs()
    gpu_usage = 0
    temp = 0
    
    if len(gpus) > 0:
        gpu = gpus[0]
        gpu_usage = gpu.load * 100
        temp = gpu.temperature
    else:
        gpu_usage = 0
        temp = 45

    mem = psutil.virtual_memory()
    ram_gb = mem.used / (1024 ** 3)

    return {
        "cpu_usage": psutil.cpu_percent(),
        "ram_usage_gb": round(ram_gb, 1),
        "gpu_usage": round(gpu_usage),
        "temp": round(temp)
    }

@app.post("/initialize")
def initialize_link():
    print("\n[SYSTEM] Initializing Neural Link...")
    
    # 1. Triggers your Faster-Whisper microphone setup
    user_text = listen_and_transcribe()
    
    # 2. If it heard you clearly, send it to Ollama
    if user_text and len(user_text) > 2:
        print(f"\n[NISHAAD]: {user_text}")
        print("[SYSTEM] Routing to Ollama neural network...")
        
        try:
            # IMPORTANT: Change "llama3" if you are using a different model (e.g., "mistral", "phi3")
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3", 
                    "prompt": user_text,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                ai_text = response.json().get("response", "")
                print(f"\n[CHIRON]: {ai_text}\n")
            else:
                print(f"[SYSTEM] Ollama Error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("\n[CRITICAL] Failed to connect to Ollama. Is the Ollama app running in the background?\n")
        except Exception as e:
            print(f"\n[CRITICAL] Error: {e}\n")
    else:
        print("\n[SYSTEM] No valid speech detected. Sequence aborted.\n")
            
    return {"status": "success", "message": "Sequence Complete"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)