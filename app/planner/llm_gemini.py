# app/planner/llm_gemini.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key from environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model (can be swapped out or configured later)
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

async def generate_creative_response(prompt: str) -> str:
    """
    Asynchronously sends a prompt to Gemini and returns the plain text response.
    """
    response = await model.generate_content_async(prompt)
    return response.text.strip()