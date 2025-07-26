# app/ui.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.planner.core import plan_from_brief
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, input: str = Form(...)):
    try:
        plan = await plan_from_brief(input)
        plan_json = json.dumps(plan.model_dump(), indent=2, ensure_ascii=False)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "plan": plan_json,
            "input": input
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })
