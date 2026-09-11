import os
from google import genai
from google.genai import types
from PIL import Image
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
You will be provided with an image of a multiple-choice question on a screen.
Your job is to read the question from the image, evaluate the options, and determine the correct answer.
CRITICAL INSTRUCTION: You must output ONLY the final answer. Do not provide explanations, do not provide conversational filler, do not repeat the question.
If the options are A, B, C, D, output just the letter of the correct option. If there are no letters, output just the correct word or phrase.
"""

def get_answer_from_image(image_path):
    if not client:
        return "Error: Gemini API not configured."
        
    try:
        img = Image.open(image_path)
        
        # Using gemini-3.8-flash as the latest stable model
        # We pass both the image and a text prompt instructing it to answer
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=[img, "What is the correct answer to the question in this image?"],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        return response.text.strip()
    except Exception as e:
        if "503" in str(e):
            return "Google API is overloaded (503). Just press the hotkey again!"
        return f"LLM Error: {e}"
