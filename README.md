# Creative Agent – GTV Project Trial

**Author**: Hannah Norman  
**Role**: Member of Technical Staff (Trial)  
**Duration**: 1 Week  
**Framework**: FastAPI | **Language**: Python 3.13.3

## 🚀 Overview

Creative Agent is a FastAPI service that transforms unstructured input into a structured creative plan for short-form video content. It powers GTV’s video generation pipeline by interpreting briefs and turning them into imaginative, audience-ready concepts.

## 📦 API

**POST /plans**

**Request**
```json
{
  "input": "We're launching a futuristic running shoe called the Acme ZG. It's lightweight, zero-gravity inspired, and designed for speed. Target audience is Gen Z runners on TikTok."
}
```

**Response (example)**
```json
{
  "title": "Zero Gravity // Fast Forward",
  "concept_summary": "A surreal TikTok skit where a Gen Z runner tests the Acme ZG shoes and literally lifts off the ground...",
  "hook": "What if shoes could literally defy gravity?",
  "visual_style": "Hyper-saturated, slow-mo running shots with floating effects.",
  "tone": "Playful, fast-paced, absurd",
  "intended_platform": "TikTok",
  "audience": "Gen Z athletes, trend-followers",
  "hashtags": ["#AcmeZG", "#ZeroGravityRun"],
  "scene_ideas": [
    "Opening in a suburban park...",
    "Friends record as the runner floats...",
    "Final shot: someone else steals the shoes and floats away."
  ]
}
```

## 🧠 Planning Logic

The agent uses a structured LLM-driven reasoning chain to:
- Interpret the brief
- Brainstorm creative directions
- Choose the most original concept
- Expand into a vivid creative plan

Supports OpenAI or Gemini APIs for text generation.

## 🛠 Setup

```bash
git clone https://github.com/YOUR_USERNAME/creative-agent.git
cd creative-agent
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🧪 Sample Test

```bash
curl -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{"input": "We’re launching a futuristic running shoe..."}'
```

## 📁 Project Structure

```
creative-agent/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── api.py               # Route handlers
│   ├── models.py            # Pydantic schemas
│   └── planner/
│       ├── core.py          # Creative planning pipeline
│       ├── prompts.py       # Prompt templates
│       └── llm.py           # LLM API calls
├── tests/
│   └── test_planner.py
├── README.md
├── .gitignore
└── requirements.txt
```

## ✅ To Do

- [ ] Implement creative planning logic
- [ ] Integrate LLM calls (OpenAI/Gemini)
- [ ] Define output schema
- [ ] Add test coverage
- [ ] Finalize API examples in README
