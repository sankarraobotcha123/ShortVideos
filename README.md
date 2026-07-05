# Edu Content Platform MVP v10

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds a **Source Safety + Originality Review workflow** on top of thumbnail helper and reusable visual assets. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, stronger TTS providers, or advanced video generation without changing the business workflow.

```text
Concept input → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Reusable Visual Assets → Thumbnail Helper → Source Safety Review → Vertical MP4 Draft → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics
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
- Reusable visual asset library:
  - Upload PNG/JPG/WebP/GIF assets
  - Store tags, license/source notes, and descriptions
  - Suggest matching assets for a package
  - Reuse matched assets inside MP4 draft scene cards
- Thumbnail helper workflow:
  - Generates thumbnail text ideas
  - Creates a manual layout guide
  - Creates Canva/CapCut thumbnail prompt
  - Exports thumbnail guide files in each package ZIP
- Source Safety + Originality Review workflow:
  - Checks source name/license/page metadata
  - Warns when copied text is marked
  - Estimates similarity between source notes and generated script
  - Produces risk level, checklist, recommendation, and downloadable markdown review
  - Exports source safety review files in each package ZIP
- Simple vertical MP4 draft generator:
  - Creates 9:16 scene-card video drafts
  - Uses matched reusable visual assets when tags match the scene
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
- Visual asset library screen
- Package detail/review screen
- Suggested visual assets on package detail
- Thumbnail helper section on package detail
- Source safety/originality review section on package detail
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
edu-content-platform-mvp-v10/
├── app/                    # FastAPI backend
│   ├── core/
│   ├── db/
│   ├── routes/
│   ├── services/
│   │   ├── asset_library_service.py
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
│   ├── asset_library/
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


## Source safety workflow

After creating a package:

1. Open the package detail page.
2. Click **Generate source safety review**.
3. Check the risk level, similarity score, checklist, and recommendation.
4. If the risk is high, rewrite the script before approving.
5. Export the package ZIP and verify these files are included:

```text
source_safety_review.md
source_safety_checklist.json
source_safety_reviews.json
```

This is not a legal verdict or full plagiarism scanner. It is an MVP publishing guardrail to prevent copied textbook-style Shorts from entering your workflow.

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
- Reusable visual assets work without any AI provider.

---

## How to test the full v10 workflow

1. Start backend.
2. Start frontend.
3. Open `http://127.0.0.1:5173`.
4. Open **Visual assets**.
5. Upload a simple image, for example a leaf diagram.
6. Use tags like `leaf, chlorophyll, photosynthesis, science`.
7. Create a package for `Why are leaves green?`.
8. Open the package detail page.
9. Confirm matching assets appear under **Suggested reusable visuals**.
10. Review/edit the script.
11. Click **Generate narration**.
12. Click **Generate assembly plan**.
13. Click **Generate video draft**.
14. Preview/download the MP4 draft.
15. Export the ZIP package.
16. Use the MP4 draft and CapCut assembly plan for manual improvement.
17. Publish manually.
18. Enter analytics weekly.

---

## Visual asset rules

Use the asset library for images you are legally allowed to reuse:

```text
Good:
- Self-created icons
- Canva-created diagrams you have rights to use
- Open-license public domain/simple icons
- Your own screenshots/diagrams

Avoid:
- Copyrighted textbook page screenshots
- Random Google images without license check
- Brand logos or characters you do not have rights to use
```

Use clear tags. Example:

```text
leaf, chlorophyll, photosynthesis, plant, science
fraction, numerator, denominator, math
noun, verb, grammar, english
```

---

## Git push

```bash
git init
git add .
git status
git commit -m "Add reusable visual asset library"
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
storage/asset_library/*
```

`.gitkeep` files inside storage folders should remain tracked.

---

## Current test status

Backend tests:

```text
9 passed
```

Frontend build:

```text
passed
```
