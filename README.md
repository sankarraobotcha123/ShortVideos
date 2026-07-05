# Edu Content Platform MVP v7

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds a **simple vertical MP4 draft generator**. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, stronger TTS providers, or advanced video generation without changing the business workflow.

```text
Concept input → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Vertical MP4 Draft → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics
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
- TTS/audio fallback system:
  - Windows SAPI provider: optional on Windows
  - pyttsx3 provider: optional, disabled by default
  - Manual recording provider: always works
- CapCut/manual assembly plan generator
- Simple vertical MP4 draft generator:
  - Creates 9:16 scene-card video drafts
  - Uses generated narration audio if available
  - Creates silent MP4 drafts if no audio exists
  - Creates manual video guide if MP4 generation fails
- Teacher Trust Score
- Human review/edit API
- Manual analytics API
- Content batch planner API
- Publishing calendar API
- ZIP export package

### Frontend

- React + Vite npm frontend
- Dashboard
- Create content package form
- Batch planner screen
- Batch detail/edit screen
- Publishing calendar screen
- Package detail/review screen
- Narration audio generation section
- CapCut/manual assembly plan section
- Vertical MP4 draft generation section
- Manual analytics entry
- AI fallback status page
- Audio fallback status page
- Script copy button
- Browser voice preview using Web Speech API

### Git

- Production-safe `.gitignore`
- Ignores `.env`, local databases, generated exports/media, virtualenvs, cache files, `node_modules`, and `dist`
- Keeps storage folders using `.gitkeep`

---

## Folder structure

```text
edu-content-platform-mvp-v7/
├── app/                    # FastAPI backend
│   ├── core/
│   ├── db/
│   ├── routes/
│   ├── services/
│   │   ├── assembly_service.py
│   │   ├── audio_service.py
│   │   ├── content_generator.py
│   │   ├── export_service.py
│   │   ├── generation_orchestrator.py
│   │   └── video_draft_service.py
│   ├── static/             # Legacy Jinja static files
│   └── templates/          # Legacy Jinja pages
├── frontend/               # React/Vite npm frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── storage/
│   ├── audio/
│   ├── exports/
│   ├── video_drafts/
│   └── final/
├── tests/
├── scripts/
├── requirements.txt
├── package.json
├── .env.example
└── .gitignore
```

---

## Run backend

From the project root:

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

## Recommended laptop `.env`

Since Ollama is not installed on your laptop, keep this simple fallback setup:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false

TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false
```

This means:

- AI generation uses the built-in template fallback.
- Audio tries Windows speech first.
- If audio generation fails, a manual recording guide is created.
- Video draft generation still works silently if audio is not available.

---

## How to test the full v7 workflow

1. Start backend.
2. Start frontend.
3. Open `http://127.0.0.1:5173`.
4. Create a content package.
5. Open the package detail page.
6. Review/edit the script.
7. Click **Generate narration**.
8. Click **Generate assembly plan**.
9. Click **Generate video draft**.
10. Preview/download the MP4 draft.
11. Export the ZIP package.
12. Use the MP4 draft and CapCut assembly plan for manual improvement.
13. Publish manually.
14. Enter analytics weekly.

---

## What the video draft generator does

The v7 video draft generator is intentionally simple.

It creates:

```text
Script + scene plan + optional narration audio → 9:16 MP4 draft
```

The draft is not meant to be final YouTube quality. It is useful for:

- Checking script timing
- Previewing scene pacing
- Seeing captions/on-screen text placement
- Sharing a rough preview before editing
- Starting from a draft instead of a blank CapCut project

### Output behavior

| Situation | Output |
|---|---|
| Narration WAV exists | MP4 draft with audio |
| No narration audio | Silent MP4 draft |
| MP4 rendering fails | Manual video draft guide `.md` |

Generated files are stored in:

```text
storage/video_drafts/
```

---

## Git push

```bash
git init
git add .
git status
git commit -m "Add vertical MP4 draft generator"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

Before pushing, confirm these are not staged:

```text
.env
.venv/
frontend/node_modules/
frontend/dist/
storage/app.db
storage/exports/
storage/audio/
storage/video_drafts/
storage/final/
```

---

## Test commands

Backend tests:

```bash
PYTHONPATH=. pytest -q
```

On Windows PowerShell:

```powershell
$env:PYTHONPATH="."
pytest -q
```

Frontend production build:

```bash
npm run frontend:install
npm run frontend:build
```

---

## Next recommended feature

After v7, the next useful step is a **reusable visual asset library**.

Build:

```text
storage/asset_library/
  science/
  math/
  icons/
  backgrounds/
```

Then update the video draft generator to use real reusable visuals instead of only text cards.

Do not build complex AI animation yet. The current priority is still:

```text
Publish better Shorts faster → collect analytics → improve content style → automate repeated work
```
