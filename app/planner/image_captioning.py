# app/planner/image_captioning.py

import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key from environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize multimodal Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")  # or "gemini-2.0-flash" for faster responses

# Prompt to guide the model's image captioning behavior
IMAGE_CAPTION_PROMPT = (
    "Describe this image creatively. Please keep your answer to a single paragraph. "
    "Be sure to mention visual styles, emotions conveyed, and any other important info you can glean from the image."
)

async def caption_image(image_bytes: bytes) -> str:
    """
    Asynchronously generates a creative caption for an image using Gemini.
    Expects image bytes (e.g. from an upload or stream).
    """
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        response = await model.generate_content_async([image, IMAGE_CAPTION_PROMPT])
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] Failed to caption image: {e}"
