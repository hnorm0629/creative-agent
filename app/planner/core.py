# app/planner/core.py

from app.models import CreativePlan

async def plan_from_brief(user_input: str) -> CreativePlan:
    # Temporary hardcoded output
    return CreativePlan(
        title="Example Title",
        concept_summary="This is a placeholder concept.",
        hook="What if shoes could defy gravity?",
        visual_style="Futuristic, vibrant, slow-mo",
        tone="Playful",
        intended_platform="TikTok",
        audience="Gen Z",
        hashtags=["#Example"],
        scene_ideas=["A runner begins floating...", "Everyone reacts..."]
    )
    