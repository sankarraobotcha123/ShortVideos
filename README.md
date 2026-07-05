# Edu Content Platform MVP — v28

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, production board, content idea backlog, series planner, bulk publishing calendar scheduling, and batch production handoff exports.

## What is new in v28

- Added **Batch Export and Production Handoff workflow**.
- Added new React page: `#/handoff`.
- Added new backend service: `app/services/batch_handoff_service.py`.
- Added new database table: `batch_handoff_runs`.
- Added API endpoints to create handoff ZIPs, list runs, download handoff ZIPs, and download the handoff report.
- Handoff ZIP includes:
  - `README_HANDOFF.md`
  - `manifest.csv`
  - `manifest.json`
  - `skipped_packages.json`
  - `packages/package-<id>.zip` for each included content package
- Added ready-only filtering so weak/unapproved packages can be skipped from editor handoff.
- Added sidebar and dashboard links for batch handoff.
- Updated version to `0.28.0` and frontend asset version to `28`.

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

## Test the handoff workflow

```text
Open http://127.0.0.1:5173/#/handoff
→ Select all packages or one batch
→ Keep ready-only enabled for production-safe export
→ Create handoff ZIP
→ Download ZIP
→ Open README_HANDOFF.md and manifest.csv
→ Use package ZIPs for CapCut/Canva/editor handoff
```

## Test/check before Git push

```bash
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
```

## Recommended Git commit

```bash
git commit -m "Add batch export and production handoff workflow"
```
