import json
import re
import asyncio
from app.logger import logger
from app.models import CreativePlan
from app.planner.prompts import creative_plan_prompt
from app.planner.llm_gemini import generate_creative_response

async def plan_from_brief(user_input: str) -> CreativePlan:
    prompt = creative_plan_prompt(user_input)
    logger.info("Generated prompt:\n%s", prompt)

    response_text = await generate_creative_response(prompt)
    logger.info("Raw LLM response:\n%s", response_text)

    clean_text = re.sub(r"^```json\n|\n```$", "", response_text.strip())
    try:
        data = json.loads(clean_text)
        logger.info("Successfully parsed JSON.")
        return CreativePlan(**data)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse LLM response as JSON", exc_info=True)
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\n\nRaw output:\n{response_text}")

# Sync wrapper for CLI usage
def plan_from_brief_sync(user_input: str) -> CreativePlan:
    return asyncio.run(plan_from_brief(user_input))
