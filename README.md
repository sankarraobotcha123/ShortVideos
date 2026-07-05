# Edu Content Platform MVP v14

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds **Analytics Dashboard Insights** on top of prompt templates, notes/quiz/flashcards/worksheets, Teacher Trust Score review, source safety, thumbnail helper, reusable visual assets, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, stronger TTS providers, or advanced video generation without changing the workflow.

```text
Concept input → Prompt Template → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Reusable Visual Assets → Thumbnail Helper → Source Safety Review → Teacher Trust Review → Learning Outputs → Vertical MP4 Draft → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics → Analytics Insights
```

---

## What is included now

### Backend

- FastAPI backend
- SQLite database
- REST API for React frontend
- Legacy Jinja UI kept as backup
- AI provider fallback system:
  - Template provider: always works
  - Transformers provider: optional local open-source model
  - Ollama provider: optional later on desktop
- Prompt Template Manager:
  - Default script templates seeded into SQLite
  - Create/edit/delete prompt templates from React UI
  - Preview prompt rendering with sample concept data
  - Select a script prompt template while creating a package
  - Store template ID, name, style, and snapshot on generated packages
- TTS/audio fallback system:
  - Windows SAPI provider: optional on Windows
  - pyttsx3 provider: optional, disabled by default
  - Manual recording provider: always works
- CapCut/manual assembly plan generator
- Reusable visual asset library
- Thumbnail helper workflow
- Source Safety + Originality Review workflow
- Teacher Trust Score Review workflow
- Notes, quiz, flashcards, and worksheet output generator
- Simple vertical MP4 draft generator
- Manual analytics API
- **Analytics Dashboard Insights API:**
  - overall analytics snapshot
  - top videos by views
  - top videos by retention
  - weak videos to improve
  - tone performance
  - prompt-template performance
  - subject performance
  - batch performance
  - weekly analytics summary
  - markdown analytics report
- Content batch planner API
- Publishing calendar API
- ZIP export package

### Frontend

- React + Vite npm frontend
- Dashboard
- Create content package form with prompt-template selection
- Prompt Template Manager screen
- Batch planner screen
- Batch detail/edit screen
- Publishing calendar screen
- Visual asset library screen
- Package detail/review screen
- Suggested visual assets on package detail
- Thumbnail helper section on package detail
- Source safety/originality review section on package detail
- Teacher Trust Score review section on package detail
- Learning outputs section on package detail
- Narration/audio section on package detail
- CapCut assembly plan section on package detail
- Vertical MP4 draft section on package detail
- Manual analytics section
- **Analytics Insights screen**
- AI fallback status screen
- Audio fallback status screen

---

## Run backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Run frontend

Open a second terminal in the project root:

```bash
npm run frontend:install
npm run frontend:dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

---

## Recommended laptop AI settings

Keep Ollama disabled on the laptop until your other desktop is ready:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

The template fallback keeps content package generation working immediately.

---

## Test workflow for v14

1. Start backend and frontend.
2. Create 3–5 content packages.
3. Add manual analytics from each package detail page.
4. Open **Analytics insights** from the sidebar.
5. Check:
   - top videos by views
   - top videos by retention
   - weak videos to improve
   - tone/template/batch performance
   - weekly summary
6. Download the analytics markdown report.

---

## Tests

```bash
python -m pytest -q
npm run frontend:build
```

Current verification for this package:

```text
18 passed
Frontend production build passed
```

---

## Git commands for v14

Use this exact commit message:

```bash
git status
git add .
git status
git commit -m "Add analytics dashboard insights workflow"
git push
```

Before committing, make sure these are not staged:

```text
.env
.venv/
frontend/node_modules/
frontend/dist/
storage/app.db
storage/exports/
storage/audio/
storage/video_drafts/
storage/asset_library/
storage/thumbnails/
storage/source_safety/
storage/trust_reviews/
storage/learning_outputs/
__pycache__/
.pytest_cache/
```

---

## Next recommended step

Next build should be:

```text
AI Provider Fallback Logging Improvements
```

Recommended commit message for the next step:

```bash
git commit -m "Improve AI provider fallback logging workflow"
```
