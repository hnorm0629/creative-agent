# app/models.py

from typing import List, Optional
from pydantic import BaseModel, Field

# Request schema: user provides an unstructured creative brief
class PlanRequest(BaseModel):
    input: str = Field(..., description="Unstructured creative brief")

# Response schema: structured video plan returned by the agent
class CreativePlan(BaseModel):
    # High-level concept
    title: str = Field(..., description="Catchy title of the video concept")
    concept_summary: str = Field(..., description="Brief summary of the overall idea")
    hook: str = Field(..., description="A compelling or strange premise to grab attention")
    audience: Optional[str] = Field(None, description="Intended or expected audience")

    # Visual tone and aesthetic
    visual_style: str = Field(..., description="Look and feel of the visuals (e.g., film noir, claymation)")
    tone: str = Field(..., description="Emotional tone (e.g., absurd, touching, chaotic)")

    # Structural elements
    scene_ideas: List[str] = Field(..., description="Outline of a few key scenes or moments")
    characters: Optional[List[str]] = Field(None, description="Names or descriptions of characters in the video")
    inspirations: Optional[List[str]] = Field(None, description="Artistic or media inspirations (e.g., directors, styles, shows)")

    # Audio elements
    dialogue_ideas: Optional[List[str]] = Field(None, description="Notable lines or spoken ideas")
    soundtrack_style: Optional[str] = Field(None, description="Musical tone, genre, or reference")
    foley_fx: Optional[List[str]] = Field(None, description="Sound effects to enhance immersion")
