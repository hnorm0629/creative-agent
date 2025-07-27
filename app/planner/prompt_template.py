# app/planner/prompt_template.py

def creative_plan_prompt(user_input: str) -> str:
    """
    Returns a full prompt string instructing the LLM to generate a vivid,
    structured creative plan for a short-form video based on the user's input.
    """

    return f"""You are a wildly creative short-form video concept generator.

Given the following user brief, generate a highly imaginative and vivid creative plan for a video idea.
The goal is to surprise, delight, and push boundaries of what's expected.

Respond ONLY in JSON format with the following fields:

- title: string
- concept_summary: string
- hook: string
- visual_style: string
- tone: string
- audience: string
- characters: list of strings
- inspirations: list of strings (e.g., directors, genres, existing media)
- dialogue_ideas: list of strings (snippets or phrases)
- soundtrack_style: string
- foley_fx: list of sound design elements
- scene_ideas: list of short scene descriptions

User brief:
\"\"\"{user_input}\"\"\"

Respond only with a single valid JSON object.
Make sure all strings (including inside lists) are enclosed in double quotes.
Do not include Markdown backticks or a code block.
"""
