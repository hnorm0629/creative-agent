# Creative Agent – GTV Project Trial

Author: Hannah Norman  
Role: Member of Technical Staff (Trial)  
Time Spent: 14 Hours  
Framework: FastAPI | Language: Python 3.13.3

## 🚀 Overview

Creative Agent is a FastAPI-based application that transforms creative briefs into detailed, structured video plans for short-form content. Designed for GTV's internal creative workflows, it generates vivid, unconventional concepts using large language models (LLMs) via a multi-step prompt-chaining pipeline.

The app includes both a web UI and JSON API, and supports media input (image or video) for richer brief generation.

## 🌐 Web UI

Access the web interface at [http://localhost:8000/](http://localhost:8000/) after running the server.

- Submit a creative brief, image, or video file.
- View the structured video plan returned by the LLM.
- UI features include loading animations, surprise prompt generation, and visual feedback.

## 🧠 Prompt Chaining Logic

By default, the planner uses a 6-stage prompt-chaining pipeline:

1. _Essence Extraction_ – distills abstract creative themes  
2. _Divergent Brainstorming_ – generates five original directions  
3. _Selection + Justification_ – picks the most creative, cinematic idea  
4. _Prompt Rewriting_ – crafts a vivid single-sentence pitch 
5. _Story Expansion_ – builds out a paragraph-long synopsis  
6. _Self-Critique & Revision_ – improves creativity and imagery  
7. _JSON Plan Drafting_ – formats final structured output  

Each step is logged with timing breakdowns.

Single-prompt mode is also supported by setting `USE_CHAINING_MODE = False` in `core.py`.

## 📦 API Endpoints

Explore and test these endpoints live at: [http://localhost:8000/docs](http://localhost:8000/docs)

### `POST /plans`
Generate a creative plan from a user-input text brief.

**Request**
```json
{
  "input": "In an abandoned subway station, an octopus successfully hails and boards a train to become the conductor on a voyage through phosphorescent deep sea worlds reflected in its underwater-themed passenger carriages."
}
```

**Response**
```json
{
  "title": "Inky's Dream Express",
  "concept_summary": "Professor Inky, a dapper clay octopus, conducts a bioluminescent coral train through the dreams of sea creatures, navigating breathtaking ecosystems and fending off leviathanic nightmares that threaten to shatter the ocean's collective consciousness.",
  "hook": "A clay octopus in a monocle boards a train made of glowing coral. Buckle up, it's about to get weird.",
  "visual_style": "Stop-motion animation with vibrant, otherworldly lighting and dreamlike textures.  Close-ups on Inky's expressive clay features.",
  "tone": "Whimsical, adventurous, with a touch of underlying dread.",
  "intended_platform": "TikTok, Instagram Reels",
  "audience": "Fans of animation, surreal storytelling, and sea life.",
  "scene_ideas": [
    "Inky meticulously polishing his pearl monocle as the coral train arrives.",
    "A carriage filled with the swirling, colorful dreams of a clownfish, transitioning seamlessly into the ancient migration route visualized by a sea turtle.",
    "Inky battling a shadowy leviathan tentacle with his conductor's baton.",
    "Close-up on Inky's worried expression as cracks appear in the coral train.",
    "The Dream Weaver Fish mending the cracks with glowing threads of bioluminescence."
  ],
  "characters": [
    "Professor Inky",
    "Dream Weaver Fish",
    "Anglerfish Nightmare",
    "Narwhal Dreamer",
    "Clownfish Child"
  ],
  "inspirations": [
    "Wes Anderson",
    "Hayao Miyazaki",
    "Fantastic Mr. Fox",
    "The Shape of Water",
    "BioShock"
  ],
  "dialogue_ideas": [
    "\"Next stop: the Coral Reef of Reverie!\"",
    "\"Mind the gap...between dreams.\"",
    "\"Hold tight, the nightmares are stirring.\"",
    "\"These dreams... they're unraveling!\""
  ],
  "soundtrack_style": "Ethereal, orchestral score blended with aquatic sound design and echoing foley effects.",
  "foley_fx": [
    "Coral train chugging",
    "Water bubbling",
    "Dream whispers",
    "Leviathan roars",
    "Cracking clay"
  ]
}
```

### `POST /plans/from-image`
Accepts an image (JPG or PNG), captions it using Gemini Vision, and feeds the result into the planner.

### `POST /plans/from-video`
Accepts a short video (MP4), captions it using Gemini Vision, and feeds the result into the planner.

### `GET /surprise`
Returns a one-sentence weird and unexpected prompt for brainstorming.

### `GET /health`
Basic health check.

## 🧪 Example Requests

You can test the API locally using `curl` commands:

### 🔤 Text Prompt
```bash
curl -X POST http://localhost:8000/plans \
  -H "Content-Type: application/json" \
  -d '{"input": "We’re launching a futuristic running shoe called the Acme ZG. It’s lightweight, zero-gravity inspired, and designed for speed. Target audience is Gen Z runners on TikTok."}'
```

### 🖼️ Image Upload
```bash
curl -X POST http://localhost:8000/plans/from-image \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

### 🎥 Video Upload
```bash
curl -X POST http://localhost:8000/plans/from-video \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_clip.mp4"
```

### 🎲 Get Surprise Prompt
```bash
curl http://localhost:8000/surprise
```

### ❤️ Health Check
```bash
curl http://localhost:8000/health
```

## 🛠 Setup Instructions

```bash
git clone https://github.com/hnorm0629/creative-agent.git  
cd creative-agent  
python3.13 -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
```

Create a `.env` file and add your LLM API key(s):
```bash
GOOGLE_API_KEY=your-gemini-key  
OPENAI_API_KEY=your-openai-key  
```

Run the development server:
```bash
uvicorn app.main:app --reload
```

Then visit [http://localhost:8000/](http://localhost:8000/) in your browser.

## ✏️ Tests

A minimal `test_planner.py` file under `app/tests/` demonstrates use of the `pytest` framework to verify planner output structure.

Run the tests:
```bash
pytest
```

## 📁 Project Structure
```
creative-agent/  
├── app/  
│   ├── main.py                   # App entrypoint and router inclusion  
│   ├── api.py                    # API route definitions  
│   ├── ui.py                     # Jinja2-based UI handler  
│   ├── models.py                 # Pydantic schemas  
│   ├── logger.py                 # Logging setup  
│   ├── planner/  
│   │   ├── core.py               # Core planning logic and JSON parsing  
│   │   ├── prompt_chain.py       # Multi-step prompt pipeline  
│   │   ├── prompt_template.py    # One-shot prompt logic 
│   │   ├── llm_openai.py         # OpenAI LLM wrapper  
│   │   ├── llm_gemini.py         # Gemini LLM wrapper  
│   │   ├── image_captioning.py   # Gemini vision model for image input  
│   │   └── video_captioning.py   # Gemini vision model for video input  
│   ├── static/  
│   │   ├── css/style.css         # App-wide styling  
│   │   ├── js/app.js             # UI interaction and fetch logic  
│   │   └── icons/                # Robot icons and assets  
│   ├── templates/  
│   │   └── index.html            # Main frontend template  
│   └── tests/
│       └── test_planner.py       # Basic unit tests  
├── .env  
├── .gitignore  
├── requirements.txt  
└── README.md  
```

## ✅ Features Completed

- Modular FastAPI backend  
- LLM prompt chaining (Gemini 1.5 Pro)  
- OpenAI surprise brief generator  
- Image and video captioning  
- Structured JSON output via Pydantic  
- Functional CLI and Swagger usage  
- Fully styled web UI with upload preview and interaction  
- Error handling, logging, and UI feedback  
- Basic test coverage

## 📌 Future Opportunities

- Add more model options (Claude, Mistral, etc.)  
- Add web streaming support for multi-turn generation
- Add user presets or creative “modes”  