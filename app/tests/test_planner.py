# tests/test_planner.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from fastapi.testclient import TestClient
from app.main import app


# ===========================================
# FastAPI integration tests
# ===========================================

client = TestClient(app)


def test_post_plan_success():
    payload = {
        "input": "An astronaut tries to start a flower shop on the moon."
    }
    response = client.post("/plans", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Check for top-level required fields in JSON plan
    assert "title" in data
    assert "scene_ideas" in data
    assert isinstance(data["scene_ideas"], list)
    assert len(data["scene_ideas"]) > 0


def test_post_plan_missing_input():
    payload = {}
    response = client.post("/plans", json=payload)
    assert response.status_code == 422  # Unprocessable Entity due to validation error


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
