# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import router as api_router
from app.ui import router as ui_router
from app.logger import logger

app = FastAPI(
    title="Creative Agent",
    description="Transforms creative briefs into structured video plans.",
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router)
app.include_router(ui_router)

logger.info("Creative Agent API started.")