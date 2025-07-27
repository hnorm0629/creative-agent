# app/planner/prompt_chain.py

import json
import time
from app.logger import logger
from app.planner.llm_gemini import generate_creative_response

# Shared JSON plan field template
JSON_FIELDS_PROMPT = """
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
"""

async def creative_plan_chained_prompt(user_input: str) -> str:
    """
    Runs a 7-step chained prompt process to generate a deeply creative,
    JSON-formatted short-form video plan from an unstructured user input.
    """

    timings = {}

    # Step 1: Extract essence of the user input
    t0 = time.perf_counter()
    essence_prompt = (
        f"You are given the following user input:\n'{user_input}'\n\n"
        "Summarize this into a high-level creative concept (1–2 sentences). "
        "Capture emotional tone, themes, or metaphors. Be abstract if needed.\n\n"
        "Respond only with the summary — do not include any explanation or commentary."
    )
    essence = await generate_creative_response(essence_prompt)
    timings["Essence Extraction"] = time.perf_counter() - t0
    logger.info("Step 1: Extracted concept:\n%s", essence)

    # Step 2: Brainstorm 5 divergent ideas
    t0 = time.perf_counter()
    brainstorm_prompt = (
        f"The concept is:\n'{essence}'\n\n"
        "Brainstorm 5 completely different short-form video ideas based on this. "
        "Each should be bizarre, cinematic, or emotionally provocative. Vary genre, setting, and tone.\n"
        f"Each idea should still relate to the original user prompt:\n'{user_input}'\n\n"
        "Respond only with the 5 ideas — do not include commentary, headers, or extra explanation."
    )
    brainstorm = await generate_creative_response(brainstorm_prompt)
    timings["Divergent Brainstorming"] = time.perf_counter() - t0
    logger.info("Step 2: Brainstormed 5 ideas:\n%s", brainstorm)

    # Step 3: Select the most original idea with justification
    t0 = time.perf_counter()
    selection_prompt = (
        f"Here are the brainstormed ideas:\n{brainstorm}\n\n"
        "Pick the most visually original idea and explain why in 2–3 sentences. "
        "Prioritize uniqueness and visual impact.\n\n"
        "Respond only with the chosen idea and justification — no intro, no conclusion, no labels."
    )
    selected = await generate_creative_response(selection_prompt)
    timings["Selection with Justification"] = time.perf_counter() - t0
    logger.info("Step 3: Selected idea + justification:\n%s", selected)

    # Step 4: Generate a cinematic one-liner
    t0 = time.perf_counter()
    prompt_gen_prompt = (
        f"Based on the selected idea:\n{selected}\n\n"
        "Write a vivid, one-sentence short-form video prompt. Make it cinematic and unpredictable.\n\n"
        "Respond only with the sentence — no preamble, no quotes, no additional commentary."
    )
    gen_prompt = await generate_creative_response(prompt_gen_prompt)
    timings["Creative Prompt Generation"] = time.perf_counter() - t0
    logger.info("Step 4: Cinematic prompt:\n%s", gen_prompt)

    # Step 5: Expand into a one-paragraph story
    t0 = time.perf_counter()
    story_prompt = (
        f"Based on this vivid one-sentence prompt:\n{gen_prompt}\n\n"
        "Expand the prompt into a full-blown, paragraph-long story synopsis with details, twists, and visually-evocative descriptions.\n"
        f"Make sure it's still rooted in the original user input:\n'{user_input}'\n\n"
        "Respond only with the story paragraph — no labels, framing, or commentary."
    )
    story = await generate_creative_response(story_prompt)
    timings["Original Story Creation"] = time.perf_counter() - t0
    logger.info("Step 5: Feedback prompt:\n%s", story)

    # Step 6: Self-critique and optional revision
    t0 = time.perf_counter()
    critique_prompt = f"""
Review the following story for creativity and originality.

Story:
{story}

To yourself, rate its creativity from 1 to 10. Can you think of any improvements that would make it even more surprising, bold, or unexpected?
If so, revise it — but keep the length to one paragraph. Preserve visual richness and connections to the user's original idea: '{user_input}'.

Respond only with the revised story paragraph (or the original if no changes are needed).
Do not include critique, ratings, or any commentary — just the paragraph.
"""
    final_story = await generate_creative_response(critique_prompt)
    timings["Final Story Completion"] = time.perf_counter() - t0
    logger.info("Step 6: Critiques and improvement:\n%s", final_story)

    # Step 7: Final JSON plan generation
    t0 = time.perf_counter()
    json_plan_prompt = f"""
You are a wildly creative short-form video concept generator.

Given the following prompt, generate a highly imaginative and vivid creative plan for a video idea.
The goal is to surprise, delight, and push boundaries of what's expected.

{JSON_FIELDS_PROMPT}

Prompt:
\"\"\"{final_story}\"\"\"

Respond only with a single valid JSON object.
Do not include any explanations, headers, or commentary.
Do not wrap your answer in Markdown or backticks.
Only output the JSON object — nothing else.
All string values (including those inside lists) must be enclosed in double quotes.
"""
    timings["Full JSON Plan"] = time.perf_counter() - t0
    logger.info("Step 7: Final JSON prompt assembled.")

    # Log timing summary
    logger.info("Timing summary (seconds):\n%s", json.dumps(timings, indent=2))

    # Return only the final prompt string for LLM
    return json_plan_prompt
