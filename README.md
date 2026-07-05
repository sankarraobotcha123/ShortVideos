# Edu Content Platform MVP v3

Shorts-first educational content creator assistant.

This version moves the main UI to a proper **npm React/Vite frontend** while keeping the **FastAPI backend** simple and reliable. Ollama is not required. The app works through the built-in template fallback and can later use Ollama or Transformers without changing the business workflow.

```text
Concept input → Script → Storyboard → Subtitles → Title/Description/Hashtags → Review → Export Package → Manual Analytics
```

---

## What is included now

### Backend

- FastAPI backend
- SQLite database
- REST API for React frontend
- Legacy Jinja UI kept as a backup
- AI provider fallback system
  - Template provider: always works
  - Transformers provider: optional local open-source model
  - Ollama provider: optional later on desktop
- Teacher Trust Score
- Human review/edit API
- Manual analytics API
- ZIP export package

### Frontend

- React + Vite npm frontend
- Dashboard
- Create content package form
- Package detail/review screen
- Manual analytics entry
- AI fallback status page
- Script copy button
- Browser voice preview using Web Speech API

### Git

- Production-safe `.gitignore`
- Ignores `.env`, local databases, generated exports/media, virtualenvs, cache files, and `node_modules`
- Keeps storage folders using `.gitkeep`

---

## Folder structure

```text
edu-content-platform-mvp-v3/
├── app/                    # FastAPI backend
│   ├── core/
│   ├── db/
│   ├── routes/
│   ├── services/
│   ├── static/             # Legacy Jinja static files
│   └── templates/          # Legacy Jinja pages
├── frontend/               # React/Vite npm frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── scripts/
├── storage/                # Local generated files; ignored by git except .gitkeep
├── tests/
├── .env.example
├── .gitignore
├── package.json            # Root helper npm scripts
└── requirements.txt
```

---

## Run backend on Windows

Open terminal in the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Backend API health check:

```text
http://127.0.0.1:8000/api/health
```

Legacy Jinja UI is still available at:

```text
http://127.0.0.1:8000
```

---

## Run npm React frontend

Open a second terminal in the project root:

```bash
npm run frontend:install
npm run frontend:dev
```

React frontend runs at:

```text
http://127.0.0.1:5173
```

The Vite dev server proxies API calls to FastAPI automatically.

You can also run inside the frontend folder:

```bash
cd frontend
npm install
npm run dev
```

---

## Recommended laptop AI settings

Because Ollama is not working on your laptop now, keep this in `.env`:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

This means:

1. Transformers is listed in the chain but disabled.
2. Template fallback always works.
3. No local LLM is required to continue development.

Later, on your desktop, enable Ollama:

```env
AI_PROVIDER_CHAIN=ollama,transformers,template
USE_OLLAMA=true
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

The app will try Ollama first and fall back safely if it fails.

---

## Main API endpoints

```text
GET    /api/packages
POST   /api/content/generate
GET    /api/content/{id}
PATCH  /api/content/{id}/review
POST   /api/content/{id}/analytics
GET    /api/settings/ai
GET    /content/{id}/export
```

---

## First test input

```text
Board/Source: NCERT / Self-written
Class/Level: Class 7
Subject: Science
Topic/Concept: Why are leaves green?
Audience: School students
Language: English
Duration: 60
Output Type: Short
Tone: Curious
Source Name: Self-written concept notes
Source License Type: Self-written / Original
Source Notes: Leaves contain chlorophyll. Chlorophyll absorbs sunlight and helps plants make food through photosynthesis. Chlorophyll reflects green light, so leaves look green.
Transformation Notes: Converted source facts into a simple original explanation with analogy, visual scenes, and a student challenge.
```

---

## Git push steps

```bash
git init
git add .
git status
git commit -m "Initial Edu Content Platform MVP"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

Before pushing, confirm `.env`, `.venv`, `node_modules`, `storage/app.db`, and generated media are not staged:

```bash
git status
```

---

## Development order from here

1. Improve React frontend screens.
2. Add content batch planner for the first 100 Shorts.
3. Add TTS/audio fallback.
4. Add CapCut/manual video assembly export format.
5. Add simple MoviePy/FFmpeg video assembly.
6. Add reusable visual asset library.
7. Enable Ollama later on desktop.

Do not build the advanced platform until the first 20–30 Shorts are created, reviewed, and measured.
