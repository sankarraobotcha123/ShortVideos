# Edu Content Platform MVP v6

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds **TTS/audio fallback + CapCut/manual assembly planning**. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, or stronger TTS providers without changing the business workflow.

```text
Concept input → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics
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
edu-content-platform-mvp-v6/
├── app/                    # FastAPI backend
│   ├── core/
│   ├── db/
│   ├── routes/
│   ├── services/
│   │   ├── assembly_service.py
│   │   ├── audio_service.py
│   │   ├── content_generator.py
│   │   ├── export_service.py
│   │   └── generation_orchestrator.py
│   ├── static/             # Legacy Jinja static files
│   └── templates/          # Legacy Jinja pages
├── frontend/               # React/Vite npm frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── scripts/
├── storage/                # Local generated files; ignored by git except .gitkeep
│   ├── audio/
│   └── exports/
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

Later, on your desktop, enable Ollama:

```env
AI_PROVIDER_CHAIN=ollama,transformers,template
USE_OLLAMA=true
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
```

The app will try Ollama first and fall back safely if it fails.

---

## Recommended laptop audio settings

Keep this in `.env`:

```env
TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false
```

How this works:

1. On Windows, the app tries built-in Windows speech first.
2. If Windows speech is not available or fails, it creates a manual recording guide.
3. Publishing does not stop because the manual guide can be used in CapCut/phone recording.

Optional later:

```env
TTS_PROVIDER_CHAIN=pyttsx3,windows_sapi,manual_recording
USE_PYTTSX3_TTS=true
```

Only enable `pyttsx3` after you confirm your system voice drivers work.

---

## Main API endpoints

```text
GET    /api/packages
POST   /api/content/generate
GET    /api/content/{id}
PATCH  /api/content/{id}/review
PATCH  /api/content/{id}/batch
POST   /api/content/{id}/analytics

POST   /api/content/{id}/audio
GET    /api/content/{id}/audio
GET    /content/{id}/audio/{asset_id}/download

POST   /api/content/{id}/assembly
GET    /api/content/{id}/assembly
GET    /content/{id}/assembly/{plan_id}/download

GET    /api/batches
POST   /api/batches
GET    /api/batches/{id}
PATCH  /api/batches/{id}

GET    /api/calendar
POST   /api/calendar
PATCH  /api/calendar/{id}
DELETE /api/calendar/{id}

GET    /api/settings/ai
GET    /api/settings/audio
GET    /content/{id}/export
```

---

## First workflow to test

1. Open the React frontend.
2. Go to **Batches**.
3. Create a batch named `First 20 Science Curiosity Shorts`.
4. Go to **Create package**.
5. Generate a Short package and assign it to that batch.
6. Open the package detail page.
7. Review/edit the script.
8. Click **Generate narration**.
9. Click **Generate assembly plan**.
10. Download the assembly plan or export the full ZIP.
11. Use `capcut_assembly_plan.md` while editing in CapCut.
12. Publish manually.
13. Add weekly analytics in the package detail page.

---

## Export ZIP contents

The ZIP can include:

```text
content_package.md
script.txt
storyboard.md
visual_prompts.md
subtitles.srt
audio_assets.json
recording guide or generated WAV
capcut_assembly_plan.md
assembly_plan.json
assembly_plans.json
package.json
```

---

## Tests

Backend tests:

```bash
python -m pytest -q
```

Frontend build:

```bash
npm run frontend:build
```

Verified for this version:

```text
Backend tests: 7 passed
Frontend production build: passed
```

---

## Git push

```bash
git add .
git status
git commit -m "Add CapCut assembly planning workflow"
git push
```

Before pushing, make sure these are not staged:

```text
.env
.venv/
frontend/node_modules/
frontend/dist/
storage/app.db
storage/exports/
storage/audio/
storage/final/
```

---

## Next recommended build

Build a **simple vertical MP4 draft generator** next.

Do not build complex animation yet. First generate a rough 9:16 draft with:

```text
scene cards + subtitles + narration audio if available
```

If no audio exists, export a silent timed draft that can still be improved in CapCut.
