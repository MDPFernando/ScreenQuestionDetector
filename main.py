import keyboard
import time
from capture import capture_screen_center
from ocr import extract_text
from llm import get_answer

def process_question():
    print("\n--- Hotkey Pressed: Processing Screen ---")
    
    # Step 1: Capture Screen
    print("1. Capturing screen...")
    image_path = capture_screen_center("test.png")
    
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

def main():
    hotkey = 'ctrl+shift+q'
    print(f"Question Detector is running in the background.")
    print(f"Press '{hotkey}' to capture the center of the screen and get an answer.")
    print("Press 'esc' to exit the application.")
    
    # Bind the hotkey to our processing function
    keyboard.add_hotkey(hotkey, process_question)
    
    # Block forever until 'esc' is pressed, keeping the script alive in the background
    keyboard.wait('esc')
    print("Exiting Question Detector.")

if __name__ == "__main__":
    main()
