# app/ui.py

"""
UI route for rendering a form-based interface and displaying the generated creative plan.
Uses Jinja2 templates and FastAPI's form handling.
"""

import json
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.logger import logger
from app.planner.core import plan_from_brief

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    """
    Renders the root form page for submitting creative prompts.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, input: str = Form(...)):
    """
    Accepts a prompt submission from the form, generates a creative plan,
    and renders the result or error message back to the same page.
    """
    try:
        plan = await plan_from_brief(input)
        plan_json = json.dumps(plan.model_dump(), indent=2, ensure_ascii=False)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "plan": plan_json,
            "input": input
        })
    except Exception as e:
        logger.exception("Failed to generate plan from form input")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })
