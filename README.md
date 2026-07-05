# Edu Content Platform MVP v13

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds a **Prompt Template Manager** on top of notes, quiz, flashcards, worksheet outputs, Teacher Trust Score review, source safety, thumbnail helper, reusable visual assets, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, stronger TTS providers, or advanced video generation without changing the business workflow.

```text
Concept input → Prompt Template → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Reusable Visual Assets → Thumbnail Helper → Source Safety Review → Teacher Trust Review → Learning Outputs → Vertical MP4 Draft → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics
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
- **Prompt Template Manager:**
  - Default script templates seeded into SQLite
  - Create/edit/delete prompt templates from React UI
  - Preview prompt rendering with sample concept data
  - Select a script prompt template while creating a package
  - Store template ID, name, style, and snapshot on generated packages
  - Export `prompt_template_snapshot.txt` inside package ZIP
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
- Human review/edit API
- Manual analytics API
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
- AI fallback status screen
- Audio fallback status screen

---

## Run backend

```bash
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

---

## Run frontend

Open a second terminal:

```bash
npm run frontend:install
npm run frontend:dev
```

Frontend runs at:

```text
http://127.0.0.1:5173
```

---

## Recommended laptop settings

Keep Ollama disabled on the laptop:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

Keep audio fallback safe:

```env
TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false
```

---

## Test workflow

1. Start backend and frontend.
2. Go to **Prompt templates**.
3. Check default templates or create a custom template.
4. Go to **Create package**.
5. Select a prompt template.
6. Generate package.
7. Open package detail and confirm **Prompt template used** appears.
8. Generate thumbnail helper, source safety review, trust review, learning outputs, narration, assembly plan, and MP4 draft as needed.
9. Export ZIP and check `prompt_template_snapshot.txt`.

---

## Tests

```bash
pytest -q
npm run frontend:build
```

Current verification for v13:

```text
17 passed
frontend build passed
```

---

## Git command for v13

```bash
git status
git add .
git status
git commit -m "Add prompt template manager workflow"
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
