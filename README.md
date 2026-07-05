# Edu Content Platform MVP v18

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds **fresh-clone setup automation** on top of release checks, demo data, analytics insights, provider logging, prompt templates, learning outputs, trust review, source safety, thumbnails, reusable visuals, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required.

```text
Concept input → Prompt Template → AI Provider Chain → Provider Logs → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Plan → Visual Assets → Thumbnail Helper → Source Safety → Teacher Trust Review → Learning Outputs → MP4 Draft → Review → Batch Planner → Calendar → Export ZIP → Manual Analytics → Analytics Insights → Demo Setup → Release Checklist → Fresh Clone Setup
```

---

## What changed in v18

- Added **fresh-clone setup automation**.
- Added cross-platform setup helper:
  - `python scripts/setup_project.py`
- Added Windows setup scripts:
  - `setup_windows.bat`
  - `setup_windows.ps1`
- Added documentation:
  - `docs/FRESH_CLONE_SETUP.md`
- Added setup guide API:
  - `GET /api/setup/guide`
  - `GET /setup/guide/download`
- Added React page:
  - `#/setup`
- Updated release checklist to include the new setup files.
- Updated version to `0.18.0` and frontend asset version to `18`.

---

## Fresh clone setup on Windows

After cloning the GitHub repo, run this from the project root:

```bat
setup_windows.bat
```

This will:

```text
create .venv
install backend requirements
copy .env.example to .env if missing
create storage folders
initialize SQLite database
seed demo data
install frontend dependencies if npm is available
```

---

## Manual backend setup

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_project.py --seed-demo
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Manual frontend setup

Open a second terminal in the project root:

```bat
npm run frontend:install
npm run frontend:dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

---

## Useful setup commands

```bash
python scripts/setup_project.py --check-only
python scripts/setup_project.py --seed-demo
python scripts/setup_project.py --reset-demo
python scripts/setup_project.py --install-backend
python scripts/setup_project.py --install-frontend
```

Open the setup guide in the React app:

```text
http://127.0.0.1:5173/#/setup
```

---

## Recommended laptop AI settings

Keep Ollama disabled on the laptop until your other desktop is ready:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

The template fallback keeps content package generation working immediately. Provider logs will show disabled providers and the successful fallback.

---

## Test workflow for v18

1. Run `setup_windows.bat`, or run the manual setup commands.
2. Start backend and frontend.
3. Open **Fresh clone setup** at `#/setup`.
4. Open **Release checklist** at `#/release`.
5. Open **MVP demo setup** at `#/demo`.
6. Confirm demo packages, provider logs, analytics insights, and exports work.

---

## Tests

```bash
python scripts/setup_project.py --check-only
python -m pytest -q
npm run frontend:build
python scripts/pre_push_check.py
```

Current backend verification for this package:

```text
24 passed
```

---

## Git commands for v18

Use this exact commit message:

```bash
git status
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
git status
git add .
git status
git commit -m "Add fresh clone setup automation"
git push
```

Before committing, make sure these are not staged:

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

---

## Next recommended step

Next build should be:

```text
Role-based login foundation
```

Recommended commit message for the next step:

```bash
git commit -m "Add role based login foundation"
```
