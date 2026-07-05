# Edu Content Platform MVP v11

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds an editable **Teacher Trust Score review workflow** on top of source safety, thumbnail helper, reusable visual assets, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required. The app works through template/manual fallbacks and can later use Ollama, Transformers, stronger TTS providers, or advanced video generation without changing the business workflow.

```text
Concept input → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Assembly Plan → Reusable Visual Assets → Thumbnail Helper → Source Safety Review → Teacher Trust Review → Vertical MP4 Draft → Review → Batch Planner → Publishing Calendar → Export Package → Manual Analytics
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
- Reusable visual asset library
- Thumbnail helper workflow
- Source Safety + Originality Review workflow
- **Teacher Trust Score Review workflow:**
  - Generates category scores for factual accuracy, age appropriateness, simplicity, visual clarity, engagement, source safety, and reviewer confidence
  - Allows manual editing of scores from React UI
  - Recalculates final trust score and recommendation
  - Updates the package trust score after review
  - Downloads/exports `teacher_trust_review.md`
- Simple vertical MP4 draft generator
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
- Teacher Trust Score review section on package detail
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
edu-content-platform-mvp-v11/
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
│   │   ├── source_safety_service.py
│   │   ├── thumbnail_service.py
│   │   ├── trust_score_service.py
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
│   ├── source_safety/
│   ├── thumbnails/
│   ├── trust_reviews/
│   └── video_drafts/
├── tests/
├── scripts/
├── requirements.txt
├── package.json
├── .env.example
└── .gitignore
```

---

## Teacher Trust Score workflow

After creating a package:

1. Open the package detail page.
2. Generate **Source Safety & Originality Review** first.
3. Click **Generate trust review**.
4. Check the category scores:
   - Factual accuracy
   - Age appropriateness
   - Simplicity
   - Visual clarity
   - Engagement
   - Source safety
   - Reviewer confidence
5. Edit scores manually if the automatic estimate is not correct.
6. Set reviewer decision:
   - `pending`
   - `approved`
   - `edit_required`
   - `rewrite_required`
   - `rejected`
7. Save the trust review.
8. Export ZIP and verify these files are included:

```text
teacher_trust_review.md
teacher_trust_checklist.json
teacher_trust_reviews.json
```

Suggested approval rule:

```text
overall_trust_score >= 85  → safe for normal review
70–84                       → needs careful human review
below 70                    → rewrite or regenerate before publishing
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

Since Ollama is not installed on your laptop, keep this fallback setup:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false

TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false
```

---

## How to test the full v11 workflow

1. Start backend.
2. Start frontend.
3. Open `http://127.0.0.1:5173`.
4. Open **Visual assets** and upload a reusable diagram/icon.
5. Create a package for `Why are leaves green?`.
6. Open the package detail page.
7. Review/edit the script.
8. Click **Generate thumbnail helper**.
9. Click **Generate source safety review**.
10. Click **Generate trust review**.
11. Edit trust scores and save the trust review.
12. Click **Generate narration**.
13. Click **Generate assembly plan**.
14. Click **Generate video draft**.
15. Export the ZIP package.
16. Publish manually.
17. Enter analytics weekly.

---

## Git push for this version

```bash
git status
git add .
git status
git commit -m "Improve teacher trust score review workflow"
git push
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
storage/asset_library/
storage/thumbnails/
storage/source_safety/
storage/trust_reviews/
__pycache__/
.pytest_cache/
```

`.gitkeep` files inside storage folders should remain tracked.

---

## Current test status

Backend tests:

```text
13 passed
```

Frontend production build:

```text
passed
```
