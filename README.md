# Edu Content Platform MVP — v27

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, production board, content idea backlog, series planner, and bulk publishing calendar scheduling.

## What is new in v27

- Added **Content Calendar Bulk Scheduling workflow**.
- Added new React page: `#/calendar/bulk`.
- Added new backend service: `app/services/calendar_bulk_service.py`.
- Added new database table: `calendar_bulk_runs`.
- Added API endpoints to preview/apply bulk schedules and view recent bulk scheduling runs.
- Added downloadable bulk scheduling report: `/calendar/bulk-schedule/download`.
- Added sidebar and dashboard links for bulk scheduling.
- Updated version to `0.27.0` and frontend asset version to `27`.

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

## Test the bulk scheduling workflow

```text
Open http://127.0.0.1:5173/#/calendar/bulk
→ Select all unscheduled packages or one batch
→ Choose start date, videos per day, spacing, playlist, and status
→ Preview schedule
→ Apply bulk schedule
→ Open Calendar to fine-tune individual dates
→ Download the bulk scheduling report
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
git commit -m "Add content calendar bulk scheduling workflow"
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
