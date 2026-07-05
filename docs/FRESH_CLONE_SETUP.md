# Fresh Clone Setup Guide

Use this guide when you clone the project from GitHub on a new laptop or desktop.

## Fast Windows setup

From the project root:

```bat
setup_windows.bat
```

This creates `.venv`, installs Python requirements, copies `.env.example` to `.env` if needed, initializes the SQLite database, seeds demo data, and installs frontend dependencies if npm is available.

## Manual Windows setup

```bat
git clone YOUR_GITHUB_REPO_URL short_videos
cd short_videos
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_project.py --seed-demo
npm run frontend:install
```

## Start development

Backend terminal:

```bat
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Frontend terminal:

```bat
npm run frontend:dev
```

Open:

```text
http://127.0.0.1:5173
```

## Cross-platform setup helper

```bash
python scripts/setup_project.py --seed-demo
```

Useful options:

```bash
python scripts/setup_project.py --check-only
python scripts/setup_project.py --install-backend
python scripts/setup_project.py --install-frontend
python scripts/setup_project.py --seed-demo
python scripts/setup_project.py --reset-demo
```

## Laptop-safe AI settings

Keep Ollama disabled on the laptop until your other desktop is ready:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

The template fallback keeps package generation working.

## Do not commit

Do not commit local/generated files:

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
__pycache__/
.pytest_cache/
```

## Git commands for this step

```bash
git status
python scripts/setup_project.py --check-only
python scripts/run_tests.py
npm run frontend:build
python scripts/pre_push_check.py
git status
git add .
git status
git commit -m "Add fresh clone setup automation"
git push
```
