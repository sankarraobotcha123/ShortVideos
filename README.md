# Edu Content Platform MVP v15

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds **AI Provider Fallback Logging** on top of analytics insights, prompt templates, notes/quiz/flashcards/worksheets, Teacher Trust Score review, source safety, thumbnail helper, reusable visual assets, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, stronger TTS providers, or advanced video generation without changing the workflow.

```text
Concept input → Prompt Template → AI Provider Chain → Provider Attempt Logs → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Reusable Visual Assets → Thumbnail Helper → Source Safety Review → Teacher Trust Review → Learning Outputs → Vertical MP4 Draft → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics → Analytics Insights
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
- **AI Provider Fallback Logging:**
  - stores every provider attempt in SQLite
  - records provider name, availability, success/failure, message, order, and duration
  - exposes provider summary and recent logs through API
  - includes provider logs in package detail and package ZIP export
  - helps safely test Ollama later without breaking the laptop workflow
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
- Analytics Dashboard Insights API
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
- Package-level AI provider attempt log
- Suggested visual assets on package detail
- Thumbnail helper section on package detail
- Source safety/originality review section on package detail
- Teacher Trust Score review section on package detail
- Learning outputs section on package detail
- Narration/audio section on package detail
- CapCut assembly plan section on package detail
- Vertical MP4 draft section on package detail
- Manual analytics section
- Analytics Insights screen
- **Provider Logs screen**
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

The template fallback keeps content package generation working immediately. The v15 provider log screen will show that Transformers is disabled and template succeeded.

---

## Test workflow for v15

1. Start backend and frontend.
2. Create a content package.
3. Open the package detail page.
4. Check **AI provider attempt log**.
5. Open **Provider logs** from the sidebar.
6. Confirm:
   - provider attempts count
   - successes/failures
   - template fallback count
   - recent provider messages
   - recommended actions
7. Export the package ZIP.
8. Confirm the ZIP includes:
   - `ai_provider_logs.json`
   - `ai_provider_log_report.md`

---

## Tests

```bash
python -m pytest -q
npm run frontend:build
```

Current verification for this package:

```text
19 passed
Frontend production build passed
```

---

## Git commands for v15

Use this exact commit message:

```bash
git status
git add .
git status
git commit -m "Improve AI provider fallback logging workflow"
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
MVP Stabilization and Demo Data Seed Workflow
```

Recommended commit message for the next step:

```bash
git commit -m "Stabilize MVP with demo data and usability fixes"
```
