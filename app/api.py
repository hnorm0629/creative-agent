# app/api.py

from fastapi import APIRouter, HTTPException, File, UploadFile
from app.logger import logger
from app.models import PlanRequest, CreativePlan
from app.planner.core import plan_from_brief
from app.planner.llm_openai import generate_surprise_brief
from app.planner.image_captioning import caption_image
from app.planner.video_captioning import caption_video

router = APIRouter()

@router.post("/plans", response_model=CreativePlan)
async def generate_plan(request: PlanRequest):
    try:
        plan = await plan_from_brief(request.input)   # Switch to prompt-chaining
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plans/from-image", response_model=CreativePlan)
async def create_plan_from_image(file: UploadFile = File(...)):
    try:
        # Step 1: Read file contentscaption_video
        contents = await file.read()
        logger.info(f"Received image upload: {file.filename}, size: {len(contents)} bytes")

        # Step 2: Get creative caption from Gemini vision
        caption = await caption_image(contents)
        logger.info("Generated caption from image:\n%s", caption)

        # Step 3: Feed caption into existing planner pipeline
        plan = await plan_from_brief(caption)
        return plan

    except Exception as e:
        logger.exception("Error generating creative plan from image")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plans/from-video", response_model=CreativePlan)
async def create_plan_from_video(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        logger.info(f"Received video upload: {file.filename}, size: {len(contents)} bytes")

        brief = await caption_video(contents)
        logger.info("Generated caption from video: %s", brief)

        plan = await plan_from_brief(brief)
        return plan
    except Exception as e:
        logger.exception("Error generating creative plan from video")
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