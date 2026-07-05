# Edu Content Platform MVP — v21

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, setup automation, and role-based permissions.

## What is new in v21

- Added permission-aware frontend action guards on top of the existing backend permission checks.
- Added shared frontend auth context and reusable `GuardedButton`, `GuardedLink`, and `PermissionNotice` components.
- Sensitive UI actions now lock with clear permission messages before the API call is attempted.
- Sidebar navigation hides role-restricted destinations when strict auth is enabled.
- Protected create package, batch, calendar, visual asset, prompt template, review, source safety, trust review, audio, assembly, video draft, learning output, analytics, and demo seed workflows in the UI.
- Role Permissions page now shows current-user allowed/blocked action cards.
- Kept local development unblocked: when `AUTH_REQUIRED=false`, frontend actions stay permissive for solo MVP work.
- Updated version to `0.21.0` and frontend asset version to `21`.

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
git commit -m "Add permission aware frontend action guards"
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
