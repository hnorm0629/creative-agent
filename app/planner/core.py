# app/planner/core.py

import json
from app.models import CreativePlan
from app.planner.prompts import creative_plan_prompt
from app.planner.llm import generate_creative_response

def plan_from_brief(user_input: str) -> CreativePlan:
    prompt = creative_plan_prompt(user_input)
    response_text = generate_creative_response(prompt)

    try:
        data = json.loads(response_text)
        return CreativePlan(**data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\n\nRaw output:\n{response_text}")
