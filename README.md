# Edu Content Platform MVP — v23

Shorts-first educational content creator with FastAPI backend, React/Vite frontend, provider fallbacks, review workflows, analytics, role-based permissions, hardened auth, and a final publishing approval gate.

## What is new in v23

- Fixed the **Prompt templates** page not opening by adding the missing `initialPromptTemplate` frontend state.
- Added **Publishing Approval Gate workflow** before marking a Short as published.
- Added publishing checklist based on script review, source safety, Teacher Trust Score, and optional production readiness items.
- Added new database table: `publishing_approvals`.
- Added new backend service: `app/services/publishing_approval_service.py`.
- Added new API endpoints for generating, listing, updating, and downloading publishing approval gates.
- Package detail page now shows the latest publishing gate and publisher decision controls.
- Marking a package or calendar entry as `published` is blocked until a publishing gate is approved.
- Export ZIP now includes publishing approval reports and checklist JSON.
- Updated version to `0.24.0` and frontend asset version to `23`.

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

## Run frontend

```bash
npm run frontend:install
npm run frontend:dev
```

Open:

```text
http://127.0.0.1:5173
```

## Test the v23 fix and new workflow

```text
1. Open #/templates and confirm the Prompt templates page opens.
2. Seed default templates if needed.
3. Create/open a content package.
4. Generate source safety review.
5. Generate Teacher Trust Score review and approve/edit scores if needed.
6. Save script review as approved.
7. Generate publishing approval gate.
8. Save publisher decision as approved if required checks pass.
9. Mark the package/calendar entry as published only after gate approval.
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
git commit -m "Add content production board workflow"
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

Add a final **content production board** that shows every package grouped by workflow status: Draft, Needs source safety, Needs trust review, Needs publishing gate, Ready to publish, Published.

Suggested next commit message:

```bash
git commit -m "Add content production board workflow"
```


## v24 update — Content Production Board

This version adds a Kanban-style production board for Shorts workflow management. It groups packages into practical production stages:

- Script Review
- Script Revision
- Production Assets
- Source Safety
- Teacher Trust Review
- Publishing Gate
- Ready to Publish
- Scheduled
- Published

The board is computed from existing package/review/calendar data and supports manual stage, priority, owner, due date, and board notes. Use it from the React UI at `#/production-board`.

Recommended commit message:

```bash
git commit -m "Add content production board workflow"
```
