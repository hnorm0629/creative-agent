# app/models.py

from pydantic import BaseModel, Field
from typing import List, Optional

class PlanRequest(BaseModel):
    input: str = Field(..., description="Unstructured creative brief")

class CreativePlan(BaseModel):
    title: str
    concept_summary: str
    hook: Optional[str] = None
    visual_style: Optional[str] = None
    tone: Optional[str] = None
    intended_platform: Optional[str] = None
    audience: Optional[str] = None
    hashtags: Optional[List[str]] = None
    scene_ideas: Optional[List[str]] = None
