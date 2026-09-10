import tkinter as tk
from tkinter import ttk
import pygetwindow as gw

class SettingsUI:
    def __init__(self, master, on_start_monitoring_callback):
        self.master = master
        self.on_start_monitoring_callback = on_start_monitoring_callback
        self.master.title("Question Detector Settings")
        self.master.geometry("400x200")
        self.master.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.selected_window_title = tk.StringVar()
        
        # UI Elements
        ttk.Label(master, text="Select Target Window:", font=("Arial", 12, "bold")).pack(pady=(20, 5))
        
        self.window_combo = ttk.Combobox(master, textvariable=self.selected_window_title, width=50, state="readonly")
        self.window_combo.pack(pady=5)
        
        ttk.Button(master, text="Refresh List", command=self.refresh_windows).pack(pady=5)
        
        start_btn = ttk.Button(master, text="Start Monitoring (Ctrl+Shift+Q)", command=self.start_monitoring)
        start_btn.pack(pady=(15, 10))
        
        self.refresh_windows()

    def refresh_windows(self):
        # Get all visible windows with titles
        windows = gw.getAllTitles()
        # Filter out empty strings and this settings window
        valid_windows = [w for w in windows if w.strip() and w != "Question Detector Settings"]
        self.window_combo['values'] = valid_windows
        if valid_windows:
            self.window_combo.current(0)

    def start_monitoring(self):
        target = self.selected_window_title.get()
        if target:
            self.on_start_monitoring_callback(target)

if __name__ == "__main__":
    def dummy_callback(target):
        print(f"Monitoring started for: {target}")
    
    root = tk.Tk()
    app = SettingsUI(root, dummy_callback)
    root.mainloop()
