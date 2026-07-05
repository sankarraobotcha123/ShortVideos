# Edu Content Platform MVP — v22

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, setup automation, role-based permissions, and hardened auth/route-guard polish.

## What is new in v22

- Added production auth hardening checks for strict-mode readiness.
- Added an **Auth hardening** page for super admins.
- Added expired-session cleanup and active-session limit enforcement.
- Added current-user password rotation that revokes existing sessions.
- Added stricter frontend route guards, so protected pages show friendly login/permission messages instead of partially loading.
- Added auth-aware API behavior that clears stale local tokens after `401` responses.
- Added secure-cookie configuration options for HTTPS deployments.
- Protected generated artifact download/export routes with permission checks.
- Updated version to `0.22.0` and frontend asset version to `22`.

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

Before strict/demo production testing, open:

```text
http://127.0.0.1:5173/#/auth-hardening
```

Then change the default password and check the hardening checklist.

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
git commit -m "Harden auth flow and frontend route guards"
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

Add final publishing approval gates so export/publish actions warn or block when source safety, trust review, and review status are not ready.

Suggested next commit message:

```bash
git commit -m "Add publishing approval gate workflow"
```
