# app/api.py

from fastapi import APIRouter, HTTPException
from app.models import PlanRequest, CreativePlan
from app.planner.core import plan_from_brief
from app.planner.llm_openai import generate_surprise_brief

router = APIRouter()

@router.post("/plans", response_model=CreativePlan)
async def generate_plan(request: PlanRequest):
    try:
        plan = await plan_from_brief(request.input)   # Switch to prompt-chaining
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/surprise")
async def get_surprise_brief():
    try:
        brief = await generate_surprise_brief()
        return {"brief": brief}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok"}