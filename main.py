import keyboard
import time
import tkinter as tk
import pygetwindow as gw
from capture import capture_window
from ocr import extract_text
from llm import get_answer
from ui_settings import SettingsUI

class QuestionDetectorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.target_window_title = None
        
        # Initialize Settings UI
        self.settings_ui = SettingsUI(self.root, self.on_start_monitoring)
        
        # Bind Esc key to close the app if pressed while UI is focused
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
    def on_start_monitoring(self, target_title):
        self.target_window_title = target_title
        print(f"Target window set to: {self.target_window_title}")
        
        # Minimize the settings window to keep it out of the way, or withdraw it
        self.root.iconify() 
        # Using iconify instead of withdraw so the user can easily bring it back to change the window
        
        hotkey = 'ctrl+shift+q'
        print(f"Monitoring active! Press '{hotkey}' to capture the window and get an answer.")
        
        # We need to ensure we don't bind multiple times if they change the window
        keyboard.unhook_all()
        keyboard.add_hotkey(hotkey, self.process_question)
        
    def process_question(self):
        if not self.target_window_title:
            return
            
        print("\n--- Hotkey Pressed: Processing Window ---")
        
        # Find the target window
        try:
            target_win = gw.getWindowsWithTitle(self.target_window_title)[0]
        except IndexError:
            print(f"Error: Could not find window with title '{self.target_window_title}'. Is it closed?")
            return
            
        # Ensure it's not minimized
        if target_win.isMinimized:
            print("Target window is minimized. Restoring...")
            target_win.restore()
            time.sleep(0.5)
            
        bbox = {
            "top": target_win.top,
            "left": target_win.left,
            "width": target_win.width,
            "height": target_win.height
        }
        
        # Step 1: Capture Window
        print(f"1. Capturing window '{self.target_window_title}'...")
        image_path = capture_window(bbox, "test.png")
        if not image_path:
            return
        
        # Step 2: Extract Text
        print("2. Extracting text via OCR...")
        extracted_text = extract_text(image_path)
        
        if not extracted_text:
            print("No text found. Aborting.")
            return
            
        # Step 3: Get Answer from LLM
        print("3. Querying Gemini for answer...")
        answer = get_answer(extracted_text)
        
        print("\n===============================")
        print(f"FINAL ANSWER: {answer}")
        print("===============================\n")

    def run(self):
        # Run the tkinter main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = QuestionDetectorApp()
    app.run()
