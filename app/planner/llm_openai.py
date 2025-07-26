# app/llm_openai.py

import os
from dotenv import load_dotenv
import openai
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_surprise_brief() -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly original idea generator for weird and viral short-form videos. "
                        "You must avoid repeating themes or concepts across responses."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Generate a **one-sentence** brief for a bizarre, surprising, or surreal short-form video concept. "
                        "Do **not** use food-related themes. Avoid common tropes. Surprise me with something unexpected, strange, or genre-defying. "
                        "Be playful, absurd, or uncanny. Limit to 35 words. No quotes, no explanation — just the brief."
                    )
                }
            ],
            temperature=1.7,
            max_tokens=60,
            top_p=0.9,
            frequency_penalty=0.8,
            presence_penalty=1.3
        )
        return response.choices[0].message.content.strip().strip('"')
    except Exception as e:
        return f"Error generating OpenAI response: {e}"

