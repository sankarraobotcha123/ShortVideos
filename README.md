# Edu Content Platform MVP — v26

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, production board, and a content idea backlog with topic scoring.

## What is new in v26

- Added **Content Idea Backlog + Topic Scoring workflow**.
- Added new React page: `#/ideas`.
- Added new backend service: `app/services/idea_backlog_service.py`.
- Added new database table: `content_ideas`.
- Added API endpoints to create, update, delete, list, download, and convert ideas into content packages.
- Added scoring fields for curiosity, evergreen value, visual potential, student value, production effort, and monetization potential.
- Added weighted topic score and priority recommendation.
- Added dashboard and sidebar links for the idea backlog.
- Demo seed now creates sample ideas also.
- Updated version to `0.26.0` and frontend asset version to `26`.

## Default local login

```text
Email   : admin@example.com
Password: ChangeMe123!
```

Open:

```text
http://127.0.0.1:5173/#/login
```

For strict permission testing, set this in `.env` and restart FastAPI:

```env
AUTH_REQUIRED=true
```

For normal local development, keep:

```env
AUTH_REQUIRED=false
```

## Run backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_project.py --seed-demo
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

## Run frontend

Open a second terminal:

```bash
npm run frontend:install
npm run frontend:dev
```

Frontend:

```text
http://127.0.0.1:5173
```

## Test the idea backlog workflow

```text
Open http://127.0.0.1:5173/#/ideas
→ Add a Shorts idea
→ Adjust the score fields
→ Mark the idea as shortlisted or ready
→ Convert the idea into a package
→ Open the generated package
→ Download the idea backlog report
```

## Pre-push checklist

```bash
git status
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
git status
git add .
git status
git commit -m "Add content series planner workflow"
git push
```

Do not commit generated/local files:

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
storage/release_reports/
__pycache__/
.pytest_cache/
```
