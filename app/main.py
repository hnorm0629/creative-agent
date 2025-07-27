# app/main.py

"""
Entrypoint for the Creative Agent FastAPI app.
Mounts API routes, UI routes, and static assets.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.logger import logger
from app.api import router as api_router
from app.ui import router as ui_router

import json

# Print JSON is readable format
class PrettyJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(content, indent=2).encode("utf-8")

# Create FastAPI app
app = FastAPI(
    title="Creative Agent",
    description="Transforms creative briefs into structured video plans.",
    version="0.1.0",
    default_response_class=PrettyJSONResponse
)

# Mount static assets (CSS, icons, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API and UI routes
app.include_router(api_router)
app.include_router(ui_router)

logger.info("Creative Agent API started.")