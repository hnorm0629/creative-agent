import json
import time
from app.logger import logger
from app.planner.llm_gemini import generate_creative_response

async def creative_plan_chained_prompt(user_input: str) -> str:
    timings = {}

    # Step 1: Essence Extraction
    t0 = time.perf_counter()
    essence_prompt = (
        f"You are given the following user input:\n'{user_input}'\n\n"
        "Summarize this into a high-level creative concept (1–2 sentences). "
        "Capture emotional tone, themes, or metaphors. Be abstract if needed."
    )
    essence = await generate_creative_response(essence_prompt)
    t1 = time.perf_counter()
    timings["Essence Extraction"] = t1 - t0
    logger.info("Step 1: Extracted concept:\n%s", essence)

    # Step 2: Divergent Brainstorming
    t0 = time.perf_counter()
    brainstorm_prompt = (
        f"The concept is:\n'{essence}'\n\n"
        "Brainstorm 5 completely different short-form video ideas based on this. "
        "Each should be bizarre, cinematic, or emotionally provocative. Vary genre, setting, and tone."
        f"But, each should also be related to the original user prompt:\n'{user_input}'\n"
    )
    brainstorm = await generate_creative_response(brainstorm_prompt)
    t1 = time.perf_counter()
    timings["Divergent Brainstorming"] = t1 - t0
    logger.info("Step 2: Brainstormed 5 ideas:\n%s", brainstorm)

    # Step 3: Selection with Justification
    t0 = time.perf_counter()
    selection_prompt = (
        f"Here are the brainstormed ideas:\n{brainstorm}\n\n"
        "Pick the most visually original idea. Justify in 2–3 sentences. "
        "Prioritize uniqueness and visual impact."
    )
    selected = await generate_creative_response(selection_prompt)
    t1 = time.perf_counter()
    timings["Selection with Justification"] = t1 - t0
    logger.info("Step 3: Selected idea + justification:\n%s", selected)

    # Step 4: Creative Prompt Generation
    t0 = time.perf_counter()
    prompt_gen_prompt = (
        f"Based on the selected idea:\n{selected}\n\n"
        "Write a vivid, one-sentence short-form video prompt. Make it cinematic and unpredictable."
    )
    gen_prompt = await generate_creative_response(prompt_gen_prompt)
    t1 = time.perf_counter()
    timings["Creative Prompt Generation"] = t1 - t0
    logger.info("Step 4: Cinematic prompt:\n%s", gen_prompt)

    # Step 5: Fleshed out storyline and concept
    t0 = time.perf_counter()
    story_prompt = (
        f"Based on this vivid, one-sentence short-form video prompt:\n{gen_prompt}\n\n"
        "Expand the prompt into a full-blown, paragraph-long story synopsis, with details, twists and turns, and visually-evocative descriptions."
        f"Again, I want this to be incredibly creative, but still traceable to the original user prompt:\n'{user_input}'\n"
    )
    story = await generate_creative_response(story_prompt)
    t1 = time.perf_counter()
    timings["Original Story Creation"] = t1 - t0
    logger.info("Step 5: Feedback prompt:\n%s", story)
    
    # Step 6: Self-Critique and Optional Revision
    t0 = time.perf_counter()
    critique_prompt = f"""
        Review the following story for creativity and originality.

        Story:
        {story}

        To yourself, rate its creativity from 1 to 10. Can you think of any improvements that would make it even more surprising, bold, or unexpected?
        If you believe a change is needed, then please make it! But keep the length of your final story to one paragraph. It is imperative this story
        is as creative and visually evocative as possible. I want readers to be able to read the story to themselves and imagine scenes and sounds and
        feel as though they are within the story themselves. Remember that the reader also offered their own ideas up front, so make sure that what
        they suggested initially is still included in the final storyline: '{user_input}'.
    """
    final_story = await generate_creative_response(critique_prompt)
    t1 = time.perf_counter()
    timings["Final Story Completion"] = t1 - t0
    logger.info("Step 6: Critiques and improvement:\n%s", story)

    # Step 7: Full JSON Plan
    t0 = time.perf_counter()

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

        Prompt: \"\"\"{final_story}\"\"\"
        Respond only with a single valid JSON object. Make sure all strings (including inside lists) are enclosed in double quotes. 
        Do not include Markdown backticks or a code block.
    """
    t1 = time.perf_counter()
    timings["Full JSON Plan"] = t1 - t0

    # Optional: parse and store for future debugging or chaining reuse
    logger.info("Timing summary (seconds):\n%s", json.dumps(timings, indent=2))

    # 🎯 Return final prompt (not the JSON)
    return json_plan_prompt
