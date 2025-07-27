import json
from app.logger import logger
from app.models import CreativePlan
from app.planner.llm_gemini import generate_creative_response

async def creative_plan_chained_prompt(user_input: str) -> CreativePlan:
    # Step 1: Essence Extraction
    essence_prompt = (
        f"You are given the following user input:\n'{user_input}'\n\n"
        "Summarize this into a high-level creative concept (1–2 sentences). "
        "Capture emotional tone, themes, or metaphors. Be abstract if needed."
    )
    essence = await generate_creative_response(essence_prompt)
    logger.info("Step 1: Extracted concept:\n%s", essence)

    # Step 2: Divergent Brainstorming
    brainstorm_prompt = (
        f"The concept is:\n'{essence}'\n\n"
        "Brainstorm 5 completely different short-form video ideas based on this. "
        "Each should be bizarre, cinematic, or emotionally provocative. Vary genre, setting, and tone."
    )
    brainstorm = await generate_creative_response(brainstorm_prompt)
    logger.info("Step 2: Brainstormed 5 ideas:\n%s", brainstorm)

    # Step 3: Selection with Justification
    selection_prompt = (
        f"Here are the brainstormed ideas:\n{brainstorm}\n\n"
        "Pick the most visually original idea. Justify in 2–3 sentences. "
        "Prioritize uniqueness and visual impact."
    )
    selected = await generate_creative_response(selection_prompt)
    logger.info("Step 3: Selected idea + justification:\n%s", selected)

    # Step 4: Creative Prompt Generation
    prompt_gen_prompt = (
        f"Based on the selected idea:\n{selected}\n\n"
        "Write a vivid, one-sentence short-form video prompt. Make it cinematic and unpredictable."
    )
    final_prompt = await generate_creative_response(prompt_gen_prompt)
    logger.info("Step 4: Cinematic prompt:\n%s", final_prompt)

    # Step 5: Full JSON Plan
    json_plan_prompt = f"""
        You are a wildly creative short-form video concept generator.

        Given the following prompt, generate a highly imaginative and vivid creative plan for a video idea. 
        The goal is to surprise, delight, and push boundaries of what's expected.

        Respond ONLY in JSON format with the following fields:

        - title: string
        - concept_summary: string
        - hook: string
        - visual_style: string
        - tone: string
        - intended_platform: string
        - audience: string
        - characters: list of strings
        - inspirations: list of strings (e.g., directors, genres, existing media)
        - dialogue_ideas: list of strings (snippets or phrases)
        - soundtrack_style: string
        - foley_fx: list of sound design elements
        - scene_ideas: list of short scene descriptions

        Prompt: \"\"\"{final_prompt}\"\"\"
        Respond only with a single valid JSON object. Make sure all strings (including inside lists) are enclosed in double quotes. 
        Do not include Markdown backticks or a code block.
        """
    return json_plan_prompt

