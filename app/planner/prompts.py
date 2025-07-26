# app/planner/prompts.py

def creative_plan_prompt(user_input: str) -> str:
    return f"""
You are a creative director for a short-form video platform.

Based on the following brief, generate a structured creative plan for a potential viral video.

Brief:
\"\"\"
{user_input}
\"\"\"

Your output should be a JSON object with the following fields:
- title
- concept_summary
- hook
- visual_style
- tone
- intended_platform
- audience
- hashtags (list of strings)
- scene_ideas (list of strings)

Respond with *only* the JSON object — no explanation.

Return the result as valid JSON. Make sure all strings (including inside lists) are enclosed in double quotes. Do not include Markdown backticks or a code block.
"""
