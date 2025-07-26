# app/api.py

from fastapi import APIRouter, HTTPException
from app.models import PlanRequest, CreativePlan
from app.planner.core import plan_from_brief

router = APIRouter()

@router.post("/plans", response_model=CreativePlan)
async def generate_plan(request: PlanRequest):
    try:
        plan = await plan_from_brief(request.input)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
