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
  "input": "A cowboy from the 1800s Wild West lost in a futuristic shopping mall in 2010."
}
```

**Response**
```json
{
  "title": "Cowboy's Cosmic Clawback",
  "concept_summary": "A time-traveling cowboy must outsmart a tech-savvy teen in a futuristic mall food court to reclaim his stolen compass, which is now powering her augmented reality game and causing reality glitches.",
  "hook": "When a cowboy from 1888 gets sucked through time into a 2010 mall, his only way back home is trapped inside a claw machine.",
  "audience": "Gen Z, millennials, fans of sci-fi comedy",
  "visual_style": "Retro-futuristic Western. Vivid, saturated colors clash with sepia-toned flashbacks. Glitch effects and augmented reality overlays.",
  "tone": "Humorous, with a touch of surrealism and Western grit.",
  "scene_ideas": [
    "Caleb lassoing an escalator",
    "Close-up of compass spinning wildly inside the claw machine",
    "Sarah battling holographic outlaws projected from her phone, oblivious to Caleb",
    "Caleb trying to pay for a churro with gold nuggets",
    "The food court transforming into a digitized prairie landscape due to the compass's power"
  ],
  "characters": [
    "Caleb (the Cowboy)",
    "Sarah (the Teen)",
    "Food Court Manager (exasperated)",
    "Talking Squirrel (AR character)"
  ],
  "inspirations": [
    "Back to the Future",
    "Wes Anderson",
    "Michel Gondry",
    "Spaghetti Westerns",
    "Vaporwave aesthetic"
  ],
  "dialogue_ideas": [
    "\"This here contraption is devil magic!\"",
    "\"OMG, it's a real-life NPC!\"",
    "\"Can I get a grande latte and a side of existential dread?\"",
    "\"This ain't my first rodeo... or century.\""
  ],
  "soundtrack_style": "8-bit Western theme with synthwave and banjo elements. Glitch hop sound effects.",
  "foley_fx": [
    "Spurs clanking on linoleum",
    "Laser gun sounds mixed with whip cracks",
    "Dial-up modem connecting sound for time travel",
    "Cinnamon pretzel crunch"
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