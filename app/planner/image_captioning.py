# app/planner/image_captioning.py

import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro")  # or gemini-2.0-flash if needed

async def caption_image(image_bytes: bytes) -> str:
    image = Image.open(BytesIO(image_bytes))
    response = await model.generate_content_async(
        [image, "Describe this image creatively. Please keep your answer to a single paragraph. \
            Be sure to mention visual styles, emotions conveyed, and any other important info you can glean from the image."]
    )
    return response.text.strip()
