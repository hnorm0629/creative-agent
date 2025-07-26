# Creative Agent – GTV Project Trial

**Author**: Hannah Norman  
**Role**: Member of Technical Staff (Trial)  
**Duration**: 1 Week  
**Framework**: FastAPI | **Language**: Python 3.13.3

## 🚀 Overview

Creative Agent is a FastAPI-based service that transforms unstructured creative briefs into structured video plans for short-form content. It supports GTV’s internal creative pipeline by generating vivid, imaginative, audience-ready concepts with the help of large language models (LLMs).

Both a JSON API and a simple web UI are provided.

## 📱 Web UI

Accessible at `http://localhost:8000/` after running the app.  
Submit a creative brief using the form to preview the generated plan.

## 📦 API

### `POST /plans`

**Request**
```json
{
  "input": "We're launching a futuristic running shoe called the Acme ZG. It's lightweight, zero-gravity inspired, and designed for speed. Target audience is Gen Z runners on TikTok."
}
```

**Response**
```json
{
  "title": "Defy Gravity with Acme ZG",
  "concept_summary": "Showcase the Acme ZG's lightweight and speed-enhancing features through visually captivating demonstrations of its 'zero-gravity' feel, targeting Gen Z runners on TikTok.",
  "hook": "Experience running like you're on the moon.",
  "visual_style": "Fast-paced, dynamic edits, vibrant neon colors, futuristic UI elements, slow-motion shots highlighting the shoe's design and flexibility.",
  "tone": "Energetic, exciting, aspirational, slightly edgy",
  "intended_platform": "TikTok",
  "audience": "Gen Z runners (16–24), fitness enthusiasts, tech-savvy individuals",
  "hashtags": ["#AcmeZG", "#ZeroGravityRunning", "#FutureofFitness", "#RunFaster", "#FitnessTok"],
  "scene_ideas": [
    "Close-up shot of the Acme ZG's unique design and materials.",
    "Runner effortlessly gliding across a track, defying gravity with each stride.",
    "Slow-motion shot of the shoe's flexible sole absorbing impact."
  ]
}
```

## 🧠 Planning Logic

The planning pipeline:
- Interprets the brief using a templated prompt
- Calls a generative LLM (Gemini 1.5 Pro)
- Parses the response into structured JSON
- Returns a `CreativePlan` with campaign-ready assets

Supports Gemini or OpenAI (with minor changes).

## 🛠 Setup

```bash
git clone https://github.com/YOUR_USERNAME/creative-agent.git
cd creative-agent
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file and add:
```bash
GOOGLE_API_KEY=your-api-key-here
```

Run the development server:
```bash
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
│   ├── main.py              # App entrypoint, logging, routing
│   ├── api.py               # API route handler for /plans
│   ├── ui.py                # HTML form for creative input
│   ├── models.py            # Pydantic schemas (PlanRequest, CreativePlan)
│   ├── planner/
│   │   ├── core.py          # Planning logic (LLM + parsing)
│   │   ├── prompts.py       # Prompt construction
│   │   └── llm.py           # Gemini API call
│   ├── templates/
│   │   └── index.html       # Jinja2 form template
│   └── static/
│       └── icons/           # UI icons and assets
├── tests/
│   └── test_planner.py
├── .env
├── README.md
├── .gitignore
└── requirements.txt
```

## ✅ Completed

- ✅ Structured API and UI routes
- ✅ Gemini LLM integration
- ✅ CreativePlan schema + prompt logic
- ✅ CLI and Swagger-compatible planner
- ✅ Markdown JSON parsing + error handling
- ✅ UI rendering with Jinja2
- ✅ Logging + error display

## 📌 Remaining Ideas

- [ ] Add prompt examples to UI
- [ ] Integrate streaming (future)
- [ ] Improve UI/UX styling
- [ ] Support multiple model backends
- [ ] Write more unit tests
