# Edu Content Platform MVP v16

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds **MVP stabilization + demo data seeding** on top of AI provider fallback logging, analytics insights, prompt templates, notes/quiz/flashcards/worksheets, Teacher Trust Score review, source safety, thumbnail helper, reusable visual assets, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required.

```text
Concept input → Prompt Template → AI Provider Chain → Provider Logs → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Plan → Visual Assets → Thumbnail Helper → Source Safety → Teacher Trust Review → Learning Outputs → MP4 Draft → Review → Batch Planner → Calendar → Export ZIP → Manual Analytics → Analytics Insights → Demo Setup / Readiness Checks
```

---

## What changed in v16

- Added **MVP Demo Setup** screen in the React frontend.
- Added backend readiness API:
  - `GET /api/system/readiness`
- Added demo data seed API:
  - `POST /api/demo/seed`
- Added demo data seed script:
  - `python scripts/seed_demo_data.py`
  - `python scripts/seed_demo_data.py --reset-demo`
- Added backend service:
  - `app/services/demo_seed_service.py`
- Demo seed creates:
  - one Science Shorts batch
  - three demo content packages
  - prompt-template usage
  - provider logs
  - source safety reviews
  - teacher trust reviews
  - thumbnail guides
  - learning outputs
  - publishing calendar rows
  - manual analytics entries
- Added readiness checks for:
  - storage folders
  - prompt templates
  - provider fallback availability
  - manual analytics availability
  - demo seed status
- Updated app version to `0.16.0` and frontend asset version to `16`.

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

## Seed demo data

Use this when you want a ready-made local demo without manually creating packages first:

```bash
python scripts/seed_demo_data.py
```

To delete only demo-seeded rows and recreate them:

```bash
python scripts/seed_demo_data.py --reset-demo
```

You can also seed from the frontend:

```text
Open React app → MVP demo setup → Seed demo data
```

The seed is safe: normal seed will not duplicate existing demo rows. Reset deletes only rows tagged as demo seed data.

---

## Recommended laptop AI settings

Keep Ollama disabled on the laptop until your other desktop is ready:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

The template fallback keeps content package generation working immediately. Provider logs will show disabled providers and the successful fallback.

---

## Test workflow for v16

1. Start backend and frontend.
2. Open **MVP demo setup**.
3. Click **Seed demo data**.
4. Open Dashboard and confirm demo packages exist.
5. Open Analytics Insights and confirm demo analytics are visible.
6. Open Provider Logs and confirm fallback attempts are visible.
7. Open a demo package and check:
   - source safety review
   - teacher trust review
   - thumbnail guide
   - learning outputs
   - export ZIP

---

## Tests

```bash
python -m pytest -q
npm run frontend:build
```

Current verification for this package:

```text
20 passed
Frontend production build passed
```

---

## Git commands for v16

Use this exact commit message:

```bash
git status
git add .
git status
git commit -m "Stabilize MVP with demo data and usability fixes"
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
Production cleanup and release checklist
```

Recommended commit message for the next step:

```bash
git commit -m "Add production cleanup and release checklist"
```
