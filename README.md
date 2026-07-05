# Edu Content Platform MVP — v33

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, production board, content idea backlog, series planner, multilingual planning, YouTube manual publishing preparation, deployment packaging guidance, and final MVP polish checks.

## What is new in v33

- Finished **Final MVP Bug-fix and UI Polish Pass**.
- Fixed frontend auth/session stability for the React + FastAPI two-port setup by using `credentials: 'include'` in the shared API request helper.
- Added new React page: `#/final-polish`.
- Added new backend service: `app/services/final_polish_service.py`.
- Added API endpoints:
  - `GET /api/final-polish/report`
  - `GET /final-polish/report/download`
- Added `docs/FINAL_MVP_POLISH.md`.
- Added keyboard focus visibility and narrow-screen UI polish in `frontend/src/styles.css`.
- Updated clean release ZIP builder to create `edu-content-platform-mvp-v33.zip`.
- Updated version to `0.33.0` and frontend asset version to `33`.
- Updated release checklist and pre-push flow for the final MVP commit.

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

## Test the final polish page

```text
Open http://127.0.0.1:5173/#/final-polish
→ Review completed final polish items
→ Check project status and local data snapshot
→ Follow manual QA steps
→ Copy final Git commands
→ Download the final MVP polish report
```

## Build a clean release ZIP

```bash
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:install
npm run frontend:build
python scripts/pre_push_check.py
python scripts/build_release_package.py
```

Default release output:

```text
dist_release/edu-content-platform-mvp-v33.zip
```

The package builder excludes `.env`, local databases, generated media, OAuth secrets, virtual environments, node_modules, frontend build output, caches, and logs.

## Recommended production overrides

For any public demo or production-like deployment, copy `.env.example` to `.env` on the server and change at least these values:

```env
ENVIRONMENT=production
AUTH_REQUIRED=true
DEFAULT_ADMIN_PASSWORD=replace-with-a-strong-password
AUTH_COOKIE_SECURE=true
CORS_ORIGINS=https://your-frontend-domain.example
DATABASE_PATH=/persistent-storage/app.db
YOUTUBE_API_ENABLED=false
YOUTUBE_DRY_RUN=true
```

## Test/check before Git push

```bash
git status
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:install
npm run frontend:build
python scripts/pre_push_check.py
python scripts/build_release_package.py
git status
git add .
git status
git commit -m "Finalize MVP bug fixes and UI polish"
git push
```

## Roadmap history

### v29 — Lightweight Multilingual Planning + Sidebar Active State

- Added multilingual planning workflow for target-language Shorts.
- Added package-linked or standalone language plans with glossary, cultural notes, voice/subtitle strategy, reviewer, checklist, and readiness score.
- Added clearer sidebar active-page highlighting and current-page chip so Dashboard/current route is visible.
- Suggested commit: `Add lightweight multilingual planning workflow and improve sidebar active state`.

### v30 — Real Provider Adapter Setup Guide

- Added provider setup guide page at `#/provider-setup`.
- Added `docs/PROVIDER_ADAPTER_SETUP.md`.
- Added hosted API placeholder environment keys while keeping hosted APIs disabled by default.
- Suggested commit: `Add real provider adapter setup guide`.

### v31 — YouTube Manual Publishing Checklist + API Prep

- Added YouTube publishing checklist page at `#/youtube-publishing`.
- Added `docs/YOUTUBE_PUBLISHING_GUIDE.md`.
- Added package readiness checks for manual upload status, publishing gate status, schedule status, and next action.
- Added safe YouTube API placeholder env keys while keeping real API upload disabled by default.
- Suggested commit: `Add YouTube publishing checklist workflow`.

### v32 — Deployment Packaging and Production Configuration

- Added deployment guide page at `#/deployment`.
- Added `docs/DEPLOYMENT_PRODUCTION_GUIDE.md`.
- Added clean release ZIP builder.
- Added production `.env` guidance and v32 release checklist updates.
- Suggested commit: `Add deployment packaging and production configuration guide`.

### v33 — Final MVP Bug-fix and UI Polish

- Fixed cross-port frontend auth cookie behavior.
- Added final polish report page at `#/final-polish`.
- Added final manual QA checklist and UI polish CSS.
- Updated release package output to v33.
- Suggested commit: `Finalize MVP bug fixes and UI polish`.

## Current roadmap status

The four major post-v29 roadmap items are complete. Future work should come from real testing and usage feedback rather than more foundation steps.
