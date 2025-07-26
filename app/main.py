# app/main.py

from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="Creative Agent",
    description="Transforms creative briefs into structured video plans.",
    version="0.1.0"
)

app.include_router(api_router)
