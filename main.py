import customtkinter as ctk
import pygetwindow as gw
import keyboard
import threading
from capture import capture_window
from ocr import extract_text
from llm import get_answer

# Modern dark theme settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Screen Question Detector")
        self.geometry("400x350")
        self.attributes("-topmost", True)  # Keeps the window always on top
        self.resizable(False, False)
        
        self.target_window = None
        self.windows_map = {}
        self.is_monitoring = False
        self.hotkey = 'ctrl+shift+q'
        
        # --- UI Layout ---
        
        self.title_label = ctk.CTkLabel(self, text="Target Window Selection", font=ctk.CTkFont(size=16, weight="bold"))
        self.title_label.pack(pady=(15, 5))
        
        self.window_combo = ctk.CTkComboBox(self, width=320, state="readonly")
        self.window_combo.pack(pady=5)
        
        self.refresh_btn = ctk.CTkButton(self, text="Refresh Windows", command=self.refresh_windows, fg_color="transparent", border_width=1, width=150)
        self.refresh_btn.pack(pady=5)
        
        self.monitor_btn = ctk.CTkButton(self, text="Start Monitoring", command=self.toggle_monitoring, width=200, height=35, font=ctk.CTkFont(size=14, weight="bold"))
        self.monitor_btn.pack(pady=(15, 10))
        
        self.result_box = ctk.CTkTextbox(self, width=360, height=110, font=ctk.CTkFont(size=16, weight="bold"), text_color="#00FF00")
        self.result_box.pack(pady=5)
        self.result_box.insert("0.0", "Waiting for target selection...")
        self.result_box.configure(state="disabled")
        
        self.refresh_windows()
        
    def refresh_windows(self):
        self.windows_map.clear()
        for w in gw.getAllWindows():
            if w.title.strip() and w.title != "Screen Question Detector":
                # Create a unique key using the title and the permanent OS Window Handle (HWND)
                # This ensures we don't lose the window if the title changes (e.g. changing tabs in a browser)
                key = f"{w.title} [ID: {w._hWnd}]"
                self.windows_map[key] = w
                
        valid_keys = list(self.windows_map.keys())
        self.window_combo.configure(values=valid_keys)
        if valid_keys:
            self.window_combo.set(valid_keys[0])
            
    def toggle_monitoring(self):
        if not self.is_monitoring:
            target_key = self.window_combo.get()
            if not target_key:
                return
            self.target_window = self.windows_map[target_key]
            self.is_monitoring = True
            
            # Switch button to red "Stop" state
            self.monitor_btn.configure(text="Stop Monitoring", fg_color="#C0392B", hover_color="#922B21")
            
            # Bind Hotkey
            keyboard.add_hotkey(self.hotkey, self.trigger_pipeline)
            self.update_result(f"Monitoring active.\nTarget locked to Window ID: {self.target_window._hWnd}\nPress {self.hotkey} to capture.")
        else:
            self.is_monitoring = False
            
            # Switch button back to normal state
            self.monitor_btn.configure(text="Start Monitoring", fg_color=["#3a7ebf", "#1f538d"], hover_color=["#325882", "#14375e"])
            
            # Unbind Hotkey
            keyboard.unhook_all()
            self.update_result("Monitoring stopped.")
            
    def update_result(self, text):
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", text)
        self.result_box.configure(state="disabled")
        
    def trigger_pipeline(self):
        # Run pipeline in a background thread so the UI doesn't freeze
        threading.Thread(target=self._process_pipeline, daemon=True).start()
        
    def _process_pipeline(self):
        self.update_result("Capturing window...")
        
        target_win = self.target_window
        
        try:
            # Check if window still exists and has valid dimensions
            if target_win.width <= 0 or target_win.height <= 0:
                self.update_result("Error: Target window is closed or invalid.")
                return
        except Exception:
            self.update_result("Error: Target window is closed or invalid.")
            return
            
        if target_win.isMinimized:
            target_win.restore()
            
        bbox = {"top": target_win.top, "left": target_win.left, "width": target_win.width, "height": target_win.height}

        
        image_path = capture_window(bbox, "test.png")
        if not image_path:
            self.update_result("Capture failed.")
            return
            
        self.update_result("Extracting text via OCR...")
        extracted_text = extract_text(image_path)
        
        if not extracted_text:
            self.update_result("No text detected in capture.")
            return
            
        self.update_result("Querying Gemini AI...")
        answer = get_answer(extracted_text)
        
        self.update_result(f"FINAL ANSWER:\n{answer}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
