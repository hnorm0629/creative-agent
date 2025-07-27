# app/planner/core.py

import json
import re
import asyncio
from pydantic import ValidationError

from app.logger import logger
from app.models import CreativePlan
from app.planner.prompt_template import creative_plan_prompt
from app.planner.prompt_chain import creative_plan_chained_prompt
from app.planner.llm_gemini import generate_creative_response

# Controls whether to use single-step or multi-step prompt generation
USE_CHAINING_MODE = True

async def plan_from_brief(user_input: str) -> CreativePlan:
    """
    Generates a CreativePlan from an unstructured user input string.
    Uses either single-shot or chained prompting depending on USE_CHAINING_MODE.
    Validates output against CreativePlan schema.
    """
    mode = "chain" if USE_CHAINING_MODE else "single"
    logger.info(f"Planning mode selected: {mode!r}")

    # Step 1: Generate prompt using selected strategy
    if USE_CHAINING_MODE:
        logger.info("Using prompt-chaining planner...")
        prompt = await creative_plan_chained_prompt(user_input)
    else:
        logger.info("Using single-shot prompt planner...")
        prompt = creative_plan_prompt(user_input)

    logger.info("Generated prompt:\n%s", prompt)

    # Step 2: Generate raw response from LLM
    response_text = await generate_creative_response(prompt)
    logger.info("Raw LLM response:\n%s", response_text)

    # Step 3: Strip Markdown formatting (```json ... ```)
    clean_text = re.sub(r"^```(?:json)?\n?|```$", "", response_text.strip(), flags=re.IGNORECASE)

    # Step 4: Parse and validate JSON
    try:
        data = json.loads(clean_text)
        logger.info("Successfully parsed JSON.")
        return CreativePlan(**data)
    except json.JSONDecodeError as e:
        logger.error("Failed to parse LLM response as JSON", exc_info=True)
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\n\nRaw output:\n{response_text}")
    except ValidationError as ve:
        logger.error("Parsed JSON but validation against CreativePlan failed", exc_info=True)
        raise ValueError(f"Validation error: {ve}\n\nParsed JSON:\n{data}")

def plan_from_brief_sync(user_input: str) -> CreativePlan:
    """
    Synchronous wrapper for CLI usage (e.g. in tests or scripts).
    """
    return asyncio.run(plan_from_brief(user_input))
