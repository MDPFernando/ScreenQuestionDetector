import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    print("Error: GEMINI_API_KEY not found in .env file.")
    client = None

# Define the strict system prompt
SYSTEM_PROMPT = """
You are an expert test-taking assistant.
You will be provided with noisy OCR text extracted from a multiple-choice question on a screen.
Your job is to identify the question, evaluate the options, and determine the correct answer.
CRITICAL INSTRUCTION: You must output ONLY the final answer. Do not provide explanations, do not provide conversational filler, do not repeat the question.
If the options are A, B, C, D, output just the letter of the correct option. If there are no letters, output just the correct word or phrase.
"""

def get_answer(ocr_text):
    if not ocr_text or not ocr_text.strip():
        return "No text detected."
        
    try:
        # Using gemini-1.5-flash as the stable production model
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=ocr_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        return response.text.strip()
    except Exception as e:
        if "503" in str(e):
            return "Google API is overloaded (503). Just press the hotkey again!"
        return f"LLM Error: {e}"

if __name__ == "__main__":
    # Test the LLM integration with a dummy question
    dummy_ocr_text = """
    Wh4t 1s th3 cap1tal of Franc3?
    A) London
    B) B3rlin
    C) Par1s
    D) Madr1d
    """
    print("Testing Gemini API with noisy dummy OCR text...")
    print(f"Input text:\n{dummy_ocr_text}")
    print("--- Gemini Answer ---")
    answer = get_answer(dummy_ocr_text)
    print(answer)
    print("---------------------")
