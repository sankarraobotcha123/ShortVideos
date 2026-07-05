# Edu Content Platform MVP — v34

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, production board, content idea backlog, series planner, multilingual planning, YouTube manual publishing preparation, deployment packaging guidance, final MVP polish checks, and local audit/test-stability tools.

## What is new in v34

- Completed a full uploaded-folder audit after the project was pushed to Git.
- Added stable backend test runner:
  - `scripts/run_tests.py`
- Added safe local artifact cleanup helper:
  - `scripts/clean_local_artifacts.py`
- Updated pre-push and release checklist commands to use the stable test runner.
- Updated clean release ZIP builder to create `edu-content-platform-mvp-v34.zip`.
- Updated version to `0.34.0` and frontend asset version to `34`.
- Kept generated/local files out of the clean release package: `.env`, local DBs, generated media, caches, `node_modules`, frontend build output, and release output.

## Audit result from this pass

Backend checks passed:

```bash
python scripts/setup_project.py --check-only
python scripts/run_tests.py
python scripts/pre_push_check.py
python scripts/build_release_package.py
```

The React/Vite build could not run inside this sandbox because the uploaded folder does not include `frontend/node_modules`, so `vite` is not installed here. On your laptop run:

```bash
npm run frontend:install
npm run frontend:build
```

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

## Local cleanup before Git push

Preview removable cache/build artifacts:

```bash
python scripts/clean_local_artifacts.py
```

Actually remove them:

```bash
python scripts/clean_local_artifacts.py --apply
```

This removes local caches and build/release outputs only. It does not delete your `.env`, database, uploaded media, or generated content storage.

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
python scripts/run_tests.py
npm run frontend:install
npm run frontend:build
python scripts/pre_push_check.py
python scripts/build_release_package.py
```

Default release output:

```text
dist_release/edu-content-platform-mvp-v34.zip
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
python scripts/run_tests.py
npm run frontend:install
npm run frontend:build
python scripts/pre_push_check.py
python scripts/build_release_package.py
git status
git add .
git status
git commit -m "Add final project audit and test stability tools"
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

### v34 — Final Project Audit and Test Stability

- Added stable test runner for backend tests.
- Added safe local cleanup helper for caches/build artifacts.
- Updated release checklist, Git commands, and release output to v34.
- Suggested commit: `Add final project audit and test stability tools`.

## Current roadmap status

The four major post-v29 roadmap items are complete. The project now also has a final audit/test-stability pass. Future work should come from real testing and usage feedback rather than more foundation steps.
