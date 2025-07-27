# app/planner/video_captioning.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro")  # Use latest available model with video support

async def caption_video(video_bytes: bytes) -> str:
    response = await model.generate_content_async(
        [
            {
                "inline_data": {
                    "data": video_bytes,
                    "mime_type": "video/mp4"
                }
            },
            "Describe this video creatively. Keep your answer to a single paragraph. \
             Mention the visuals, sounds, emotions, pacing, and anything else that would help inspire a short-form video idea."
        ]
    )
    return response.text.strip()
