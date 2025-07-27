# app/planner/video_captioning.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load Gemini API key from environment
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini multimodal model with video support
model = genai.GenerativeModel("gemini-2.5-pro")  # Or gemini-2.0-flash if latency is critical

# Prompt to guide the video captioning behavior
VIDEO_CAPTION_PROMPT = (
    "Describe this video creatively. Keep your answer to a single paragraph. "
    "Mention the visuals, sounds, emotions, pacing, and anything else that would help inspire a short-form video idea."
)

async def caption_video(video_bytes: bytes) -> str:
    """
    Asynchronously generates a creative paragraph describing a video using Gemini.
    Expects raw video bytes (MP4 format).
    """
    try:
        response = await model.generate_content_async([
            {
                "inline_data": {
                    "data": video_bytes,
                    "mime_type": "video/mp4"
                }
            },
            VIDEO_CAPTION_PROMPT
        ])
        return response.text.strip()
    except Exception as e:
        return f"[Gemini Error] Failed to caption video: {e}"
