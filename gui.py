import customtkinter as ctk
import requests
import threading
import time
import os
from tkinter import filedialog, messagebox

# --- Configuration ---
BACKEND_URL = "http://localhost:5000"
USER_BUBBLE_COLOR = "#4F46E5"  # Indigo
AI_BUBBLE_COLOR = "#FFFFFF"    # White
SIDEBAR_COLOR = "#0F172A"      # Dark Slate

class StudyAssistantGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MindMerge RAG Assistant (TinyLlama)")
        self.geometry("1150x850")
        
        # Configure layout (Sidebar | Main Workspace)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Left Panel) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=SIDEBAR_COLOR, border_width=1, border_color="#1E293B")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Sidebar Header: Logo
        self.logo = ctk.CTkLabel(self.sidebar, text="✨ MindMerge", font=ctk.CTkFont(size=24, weight="bold", slant="italic"), text_color="white")
        self.logo.pack(pady=(40, 30), padx=20)

        # New Discussion Button
        self.new_btn = ctk.CTkButton(self.sidebar, text="+ NEW DISCUSSION", fg_color="#4F46E5", hover_color="#4338CA", corner_radius=12, height=45, font=ctk.CTkFont(weight="bold"), command=self.clear_chat)
        self.new_btn.pack(pady=10, padx=20, fill="x")

        # Knowledge Base Label
        self.lib_lbl = ctk.CTkLabel(self.sidebar, text="KNOWLEDGE BASE", font=ctk.CTkFont(size=10, weight="bold"), text_color="#64748B")
        self.lib_lbl.pack(pady=(30, 5), padx=25, anchor="w")

        # Scrollable Document List
        self.doc_frame = ctk.CTkScrollableFrame(self.sidebar, height=220, fg_color="transparent")
        self.doc_frame.pack(fill="x", padx=10)
        
        # Action Buttons
        self.add_file_btn = ctk.CTkButton(self.sidebar, text="📁 Add Lecture PDF", font=ctk.CTkFont(size=12, weight="bold"), fg_color="#1E293B", border_width=1, border_color="#334155", hover_color="#334155", command=self.upload_file)
        self.add_file_btn.pack(pady=(20, 5), padx=20, fill="x")

        # System Info Box - Updated to reflect TinyLlama
        self.info_box = ctk.CTkFrame(self.sidebar, fg_color="#1E293B", corner_radius=15)
        self.info_box.pack(side="bottom", fill="x", padx=20, pady=30)
        self.info_lbl = ctk.CTkLabel(self.info_box, text="Embed: Ollama (Nomic)\nEngine: FAISS Local\nModel: Ollama (TinyLlama)", font=ctk.CTkFont(size=10), text_color="#94A3B8", justify="left")
        self.info_lbl.pack(padx=15, pady=15)

        # --- Main Workspace (Right Panel) ---
        self.workspace = ctk.CTkFrame(self, fg_color="#F8FAFC", corner_radius=40)
        self.workspace.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.workspace.grid_rowconfigure(1, weight=1)
        self.workspace.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ctk.CTkFrame(self.workspace, height=80, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", padx=40, pady=(20, 0))
        
        self.title_lbl = ctk.CTkLabel(self.header, text="Academic AI Assistant", font=ctk.CTkFont(size=22, weight="bold"), text_color="#1E293B")
        self.title_lbl.pack(side="left")

        self.status_lbl = ctk.CTkLabel(self.header, text="● Online", font=ctk.CTkFont(size=12, weight="bold"), text_color="#10B981")
        self.status_lbl.pack(side="right")

        # Chat Canvas
        self.chat_canvas = ctk.CTkScrollableFrame(self.workspace, fg_color="transparent")
        self.chat_canvas.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Input Dock at bottom
        self.dock = ctk.CTkFrame(self.workspace, height=110, fg_color="white", corner_radius=30, border_width=1, border_color="#E2E8F0")
        self.dock.grid(row=2, column=0, sticky="ew", padx=60, pady=(0, 45))
        self.dock.grid_columnconfigure(0, weight=1)

        self.entry = ctk.CTkEntry(self.dock, placeholder_text="Ask your tutor anything...", height=60, border_width=0, fg_color="transparent", font=ctk.CTkFont(size=16))
        self.entry.grid(row=0, column=0, padx=25, pady=10, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.dock, text="Send", width=100, height=50, corner_radius=18, fg_color="#4F46E5", font=ctk.CTkFont(weight="bold"), command=self.send_message)
        self.send_btn.grid(row=0, column=1, padx=20)

        # Welcome message
        self.add_ai_bubble("Hello! Your CS Study Assistant is ready. Using your local TinyLlama model for fast, local queries.")

    def set_status(self, text, color="#10B981"):
        self.status_lbl.configure(text=text, text_color=color)

    def add_doc_entry(self, name):
        doc = ctk.CTkLabel(self.doc_frame, text=f"📄 {name}", font=ctk.CTkFont(size=12), text_color="#CBD5E1", anchor="w")
        doc.pack(fill="x", padx=15, pady=2)

    def add_user_bubble(self, message):
        bubble = ctk.CTkLabel(self.chat_canvas, text=message, fg_color=USER_BUBBLE_COLOR, text_color="white", corner_radius=20, wraplength=500, padx=20, pady=12, justify="left")
        bubble.pack(anchor="e", pady=10, padx=(100, 25))
        self.chat_canvas._parent_canvas.yview_moveto(1.0)

    def add_ai_bubble(self, message):
        container = ctk.CTkFrame(self.chat_canvas, fg_color="transparent")
        container.pack(anchor="w", pady=10, padx=(25, 100))
        
        # Outer frame for border/shadow effect
        bubble_frame = ctk.CTkFrame(container, fg_color="#FFFFFF", corner_radius=20, border_width=1, border_color="#E2E8F0")
        bubble_frame.pack(anchor="w")
        
        bubble = ctk.CTkLabel(bubble_frame, text=message, text_color="#1E293B", wraplength=550, padx=20, pady=12, justify="left")
        bubble.pack()
        
        ts = ctk.CTkLabel(container, text=f"Tutor • {time.strftime('%H:%M')}", font=ctk.CTkFont(size=10), text_color="#94A3B8")
        ts.pack(anchor="w", padx=10, pady=2)
        self.after(100, lambda: self.chat_canvas._parent_canvas.yview_moveto(1.0))

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            name = os.path.basename(file_path)
            self.set_status("● Indexing...", "#F59E0B")
            threading.Thread(target=self.perform_upload, args=(file_path, name), daemon=True).start()

    def perform_upload(self, file_path, name):
        """Sends PDF to Node.js backend for indexing"""
        try:
            with open(file_path, "rb") as f:
                response = requests.post(f"{BACKEND_URL}/upload", files={"file": (name, f)}, timeout=180)
            
            if response.status_code == 200:
                self.after(0, lambda: self.add_doc_entry(name))
                self.after(0, lambda: self.set_status("● Online"))
                self.after(0, lambda: messagebox.showinfo("Success", f"'{name}' indexed into local knowledge base."))
            else:
                self.after(0, lambda: self.set_status("● Error", "#EF4444"))
                self.after(0, lambda: messagebox.showerror("Error", "Backend failed to process PDF."))
        except Exception as e:
            self.after(0, lambda: self.set_status("● Offline", "#EF4444"))
            self.after(0, lambda: messagebox.showerror("Connection Error", "Is the Node.js server running?"))

    def clear_chat(self):
        for widget in self.chat_canvas.winfo_children():
            widget.destroy()
        self.add_ai_bubble("Discussion reset. What can I explain next?")

    def send_message(self):
        user_text = self.entry.get().strip()
        if not user_text: return

        self.add_user_bubble(user_text)
        self.entry.delete(0, "end")
        self.send_btn.configure(state="disabled")
        threading.Thread(target=self.fetch_ai_response, args=(user_text,), daemon=True).start()

    def fetch_ai_response(self, text):
        """Requests response from Node.js backend using TinyLlama"""
        try:
            response = requests.post(f"{BACKEND_URL}/chat", json={"message": text}, timeout=120)
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get("reply", "No response content.")
                sources = data.get("sources", [])
                
                source_text = f"\n\n📍 Sources: {', '.join(sources)}" if sources else ""
                full_message = f"{reply}{source_text}"
                
                self.after(0, lambda: self.add_ai_bubble(full_message))
            else:
                self.after(0, lambda: self.add_ai_bubble("Error: Local AI failed to respond. Check terminal."))
        except Exception as e:
            self.after(0, lambda: self.add_ai_bubble("Connection Error: Is Ollama running tinyllama?"))
        finally:
            self.after(0, lambda: self.send_btn.configure(state="normal"))

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = StudyAssistantGUI()
    app.mainloop()