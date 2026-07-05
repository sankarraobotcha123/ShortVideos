# Edu Content Platform MVP — v32

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, production board, content idea backlog, series planner, multilingual planning, YouTube manual publishing preparation, and deployment packaging guidance.

## What is new in v32

- Added **Deployment Packaging and Production Configuration Guide**.
- Added new React page: `#/deployment`.
- Added new backend service: `app/services/deployment_config_service.py`.
- Added API endpoints:
  - `GET /api/deployment/guide`
  - `GET /deployment/guide/download`
- Added `docs/DEPLOYMENT_PRODUCTION_GUIDE.md`.
- Added clean release ZIP builder: `scripts/build_release_package.py`.
- Added production-focused `.env.example` keys:
  - `ENVIRONMENT`
  - `PUBLIC_FRONTEND_URL`
  - `PUBLIC_API_URL`
  - `TRUST_PROXY_HEADERS`
  - `LOG_LEVEL`
- Updated version to `0.32.0` and frontend asset version to `32`.
- Updated release checklist and pre-push flow for deployment packaging.

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

## Test the new deployment guide

```text
Open http://127.0.0.1:5173/#/deployment
→ Review production .env recommendations
→ Check protected paths
→ Copy packaging commands
→ Download the deployment guide markdown
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
dist_release/edu-content-platform-mvp-v32.zip
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
git commit -m "Add deployment packaging and production configuration guide"
git push
```

## Recent roadmap history

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
