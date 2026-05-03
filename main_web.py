import streamlit as st
import threading
import queue
import base64
from stt_handler import listen_and_transcribe
from brain import parse_intent
from actions import ACTION_MAP
from voice_engine import speak

# --- UI CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="CHIRON INTELLIGENCE INTERFACE", layout="wide", initial_sidebar_state="collapsed")

# --- UI STATE HANDLING ---
if 'stt_text' not in st.session_state: st.session_state.stt_text = "Awaiting connection..."
if 'llm_response' not in st.session_state: st.session_state.llm_response = "Interface Ready."
if 'listening' not in st.session_state: st.session_state.listening = False

# --- HUD FUNCTIONALITY ---
def trigger_stt():
    st.session_state.listening = True
    st.session_state.stt_text = "LISTENING..."
    threading.Thread(target=process_voice).start()

def process_voice():
    # 1. Listen
    user_speech = listen_and_transcribe()
    
    if user_speech:
        st.session_state.stt_text = user_speech
        
        # 2. Think
        decision = parse_intent(user_speech)
        st.session_state.llm_response = decision
        
        # 3. Act
        if "ACTION:" in decision:
            action_part = decision.replace("ACTION:", "").strip().split("|")
            cmd = action_part[0]
            arg = action_part[1] if len(action_part) > 1 else "local"
            if cmd in ACTION_MAP:
                result = ACTION_MAP[cmd](arg)
                st.session_state.llm_response = result
                speak(result)
        else:
            # Normal chat
            speak(decision)

    st.session_state.listening = False

# --- INJECT ADVANCED HUD CSS ---
# This CSS is engineered to mimic image_0b6b89.png precisely
hud_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');

/* Define HUD variables based on your reference */
:root {
    --hud-glow: #A855F7;
    --hud-bg: #000000;
    --hud-card: rgba(15, 15, 15, 0.85);
    --hud-border: #1A1A1A;
}

/* 1. Global Reset & HUD Background (Hex Grid simulated) */
.stApp {
    background-color: var(--hud-bg);
    color: var(--hud-glow);
    font-family: 'JetBrains Mono', monospace;
    background-image: 
        linear-gradient(rgba(168, 85, 247, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(168, 85, 247, 0.05) 1px, transparent 1px);
    background-size: 50px 50px; /* Simulated grid */
}

/* Hide standard Streamlit elements for full immersion */
[data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stFooter"] { display: none !important; }
.block-container { padding-top: 2rem; }

/* 2. HUD Box Styling (Glassmorphism & Neon Border) */
.hud-box {
    border: 1px solid var(--hud-border);
    background-color: var(--hud-card);
    border-radius: 5px; /* Angled corners simulated by small radius */
    padding: 15px;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.1);
    position: relative;
    overflow: hidden;
    margin-bottom: 20px;
}

/* Glowing accent lines (top-left/bottom-right) */
.hud-box::before {
    content: ''; position: absolute; top: 0; left: 0; width: 30px; height: 1px; background: var(--hud-glow); box-shadow: 0 0 5px var(--hud-glow);
}
.hud-box::after {
    content: ''; position: absolute; bottom: 0; right: 0; width: 30px; height: 1px; background: var(--hud-glow); box-shadow: 0 0 5px var(--hud-glow);
}

/* 3. Typography & Titles */
h1, h2, h3, h4 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--hud-glow) !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.hud-title { font-size: 10px; color: var(--hud-border); font-weight: bold; }
.hud-data { color: #E5E7EB; font-size: 14px; }

/* 4. The Pulsing Central Orb */
.orb-container { display: flex; justify-content: center; align-items: center; height: 350px; }
.orb {
    width: 250px; height: 250px; border-radius: 50%;
    background: radial-gradient(circle, var(--hud-glow) 0%, #3B0764 60%, var(--hud-bg) 100%);
    box-shadow: 0 0 50px rgba(168, 85, 247, 0.6);
    animation: orb-pulse 3s infinite;
}
@keyframes orb-pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 50px rgba(168, 85, 247, 0.6); }
    50% { transform: scale(1.03); box-shadow: 0 0 70px rgba(168, 85, 247, 0.8); }
}

/* 5. Custom Button (Transparent with Glow) */
div.stButton > button {
    background: transparent !important;
    border: 1px solid var(--hud-glow) !important;
    color: var(--hud-glow) !important;
    border-radius: 5px !important;
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 1px;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.2);
    transition: 0.3s;
}
div.stButton > button:hover {
    background: rgba(168, 85, 247, 0.1) !important;
    box-shadow: 0 0 15px var(--hud-glow);
}

/* Specific styling for the 'Listening' state */
.listening-btn { border-color: #EF4444 !important; color: #EF4444 !important; box-shadow: 0 0 15px #EF4444 !important;}

</style>
"""
st.markdown(hud_style, unsafe_allow_html=True)

# --- HUD CONTENT LAYOUT ---
# We use st.columns to recreate the spatial distribution from the reference image
main_col1, main_col2, main_col3 = st.columns([1, 1.5, 1])

# Left Column (Location & Vital)
with main_col1:
    st.markdown("""
        <div class="hud-box">
            <div class="hud-title">NODE // LOCATION</div>
            <div class="hud-data">Vellore, IN<br>LAT: 12.9257° N<br>LNG: 79.1352° E</div>
        </div>
        <div class="hud-box">
            <div class="hud-title">SYSTEM VITAL</div>
            <div class="hud-data">Core: STABLE<br>RTX 3050: UTIL 45%<br>VRAM: 1.8GB / 4GB</div>
        </div>
    """, unsafe_allow_html=True)

# Center Column (The Orb & Primary Input)
with main_col2:
    st.markdown("""
        <div class="orb-container">
            <div class="orb"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; margin-top: -80px;'>CHIRON</h2>", unsafe_allow_html=True)
    
    # Custom button class handling based on listening state
    btn_label = "LISTENING..." if st.session_state.listening else "INITIALIZE NEURAL LINK"
    btn_class = "listening-btn" if st.session_state.listening else ""
    
    st.button(btn_label, use_container_width=True, on_click=trigger_stt)

# Right Column (Logs & Activity)
with main_col3:
    st.markdown(f"""
        <div class="hud-box" style="height: 250px;">
            <div class="hud-title">ACTIVITY MONITOR</div>
            <p style="color: #6EE7B7;">> {st.session_state.stt_text[:100]}</p>
        </div>
        <div class="hud-box" style="height: 150px;">
            <div class="hud-title">SYSTEM_LOG // J.A.R.V.I.S. MODE</div>
            <p style="color: #D1D5DB; font-size: 12px;">Initializing Core... Secure.<br>User: Nishaad Paunikar authenticated.</p>
        </div>
    """, unsafe_allow_html=True)