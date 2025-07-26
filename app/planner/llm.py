# app/planner/llm.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_creative_response(prompt: str, temperature: float = 0.9) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a brilliant, creative short-form video director."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()
