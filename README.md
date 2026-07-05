# Edu Content Platform MVP — v20

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, setup automation, and role-based permissions.

## What is new in v20

- Added permission enforcement foundation for sensitive creator API actions.
- Protected create/edit/review/generate/manage routes with role permissions.
- Added `/api/auth/permissions` for the frontend permission matrix.
- Added React **Permissions** page.
- Fixed the frontend sidebar issue by making the sidebar scroll-safe and grouping navigation links.
- Kept local development unblocked: when `AUTH_REQUIRED=false`, protected routes stay permissive for solo MVP work.
- When `AUTH_REQUIRED=true`, protected routes require login and the correct role permission.
- Updated version to `0.20.0` and frontend asset version to `20`.

## Default local login

After database setup, use:

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

## Run frontend

```bash
npm run frontend:install
npm run frontend:dev
```

Open:

```text
http://127.0.0.1:5173
```

## Pre-push checks

```bash
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
```

## Git commands for this step

```bash
git status
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
git status
git add .
git status
git commit -m "Enforce role permissions on creator workflows and fix sidebar navigation"
git push
```

Before committing, confirm these are not staged:

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

## Next recommended step

Feature polish for protected workflows: show permission-aware disabled actions in the frontend and add stricter publish approval rules.

Suggested next commit message:

```bash
git commit -m "Add permission aware frontend action guards"
```
