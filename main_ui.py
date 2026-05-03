import customtkinter as ctk
import threading
import queue
from stt_handler import listen_and_transcribe
from brain import parse_intent
from actions import ACTION_MAP
from voice_engine import speak

class PremiumChiron(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("CHIRON v2.0")
        self.geometry("1100x700")
        self.configure(fg_color="#000000") # Pure black background
        
        # --- Theme Colors ---
        self.accent_purple = "#A855F7"
        self.dark_card = "#0F0F0F"
        self.text_dim = "#9CA3AF"

        # --- Grid Configuration ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Navigation/Status) ---
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color=self.dark_card, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="CHIRON", font=("Orbitron", 28, "bold"), text_color=self.accent_purple)
        self.logo.pack(pady=40)

        self.status_card = ctk.CTkFrame(self.sidebar, fg_color="#1A1A1A", height=100)
        self.status_card.pack(padx=20, fill="x", pady=20)
        self.status_title = ctk.CTkLabel(self.status_card, text="SYSTEM STATUS", font=("DM Sans", 12), text_color=self.text_dim)
        self.status_title.pack(pady=(10,0))
        self.status_val = ctk.CTkLabel(self.status_card, text="ONLINE", font=("DM Sans", 16, "bold"), text_color="#10B981")
        self.status_val.pack(pady=(0,10))

        # --- Main Content Area ---
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        # Chat Section (The Terminal Glass)
        self.chat_frame = ctk.CTkFrame(self.content, fg_color=self.dark_card, corner_radius=15, border_width=1, border_color="#262626")
        self.chat_frame.pack(fill="both", expand=True)
        
        self.chat_display = ctk.CTkTextbox(self.chat_frame, fg_color="transparent", font=("DM Sans", 16), text_color="#E5E7EB", border_width=0)
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=20)

        # Bottom Control Section
        self.control_bar = ctk.CTkFrame(self.content, fg_color="transparent", height=100)
        self.control_bar.pack(fill="x", pady=(20, 0))

        self.mic_button = ctk.CTkButton(
            self.control_bar, 
            text="INITIALIZE NEURAL LINK", 
            font=("DM Sans", 14, "bold"),
            fg_color=self.accent_purple, 
            hover_color="#7E22CE",
            height=50,
            corner_radius=25,
            command=self.start_voice_thread
        )
        self.mic_button.pack(side="right", padx=10)

        self.input_status = ctk.CTkLabel(self.control_bar, text="Ready for input...", font=("DM Sans", 14), text_color=self.text_dim)
        self.input_status.pack(side="left", padx=10)

        # Threading Queue
        self.update_queue = queue.Queue()
        self.after(100, self.process_queue)

    def log(self, sender, text):
        color = self.accent_purple if sender == "CHIRON" else "#FFFFFF"
        self.chat_display.insert("end", f"{sender}: ", (sender,))
        self.chat_display.insert("end", f"{text}\n\n")
        self.chat_display.see("end")

    def process_queue(self):
        try:
            while True:
                msg_type, content = self.update_queue.get_nowait()
                if msg_type == "status":
                    self.input_status.configure(text=content)
                    if "LISTENING" in content: self.mic_button.configure(fg_color="#EF4444", text="LISTENING...")
                    else: self.mic_button.configure(fg_color=self.accent_purple, text="INITIALIZE NEURAL LINK")
                elif msg_type == "chat":
                    sender, text = content
                    self.log(sender, text)
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def start_voice_thread(self):
        self.mic_button.configure(state="disabled")
        threading.Thread(target=self.voice_loop, daemon=True).start()

    def voice_loop(self):
        self.update_queue.put(("status", "LISTENING..."))
        user_speech = listen_and_transcribe()
        
        if user_speech:
            self.update_queue.put(("chat", ("YOU", user_speech)))
            self.update_queue.put(("status", "ANALYZING..."))
            
            decision = parse_intent(user_speech)
            
            if "ACTION:" in decision:
                action_part = decision.replace("ACTION:", "").strip().split("|")
                cmd, arg = action_part[0], action_part[1] if len(action_part) > 1 else "local"
                if cmd in ACTION_MAP:
                    result = ACTION_MAP[cmd](arg)
                    self.update_queue.put(("chat", ("CHIRON", result)))
                    speak(result)
            else:
                self.update_queue.put(("chat", ("CHIRON", decision)))
                speak(decision)

        self.update_queue.put(("status", "READY"))
        self.mic_button.configure(state="normal")

if __name__ == "__main__":
    app = PremiumChiron()
    app.mainloop()