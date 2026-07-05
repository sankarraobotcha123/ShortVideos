# Edu Content Platform MVP v19

Shorts-first educational content creator assistant.

This version uses a **FastAPI backend** and **React/Vite npm frontend**, keeps Jinja as a backup UI, and adds a **role-based login foundation** on top of fresh-clone setup automation, release checks, demo data, analytics insights, provider logging, prompt templates, learning outputs, trust review, source safety, thumbnails, reusable visuals, audio fallback, assembly planning, and MP4 draft generation. Ollama is not required.

```text
Login/Roles → Concept input → Prompt Template → AI Provider Chain → Provider Logs → Script → Storyboard → Subtitles → Narration Audio/Guide → CapCut Plan → Visual Assets → Thumbnail Helper → Source Safety → Teacher Trust Review → Learning Outputs → MP4 Draft → Review → Batch Planner → Calendar → Export ZIP → Manual Analytics → Analytics Insights → Demo Setup → Release Checklist → Fresh Clone Setup
```

---

## What changed in v19

- Added **role-based login foundation**.
- Added local default admin bootstrap.
- Added secure password hashing using PBKDF2-SHA256.
- Added bearer-token session table.
- Added auth/user API routes:
  - `POST /api/auth/login`
  - `POST /api/auth/logout`
  - `GET /api/auth/me`
  - `GET /api/auth/status`
  - `GET /api/auth/users`
  - `POST /api/auth/users`
  - `PATCH /api/auth/users/{user_id}`
- Added React pages:
  - `#/login`
  - `#/users`
- Added roles:
  - `super_admin`
  - `content_admin`
  - `script_reviewer`
  - `video_editor`
  - `publisher`
  - `viewer`
- Added auth token handling in the React API client.
- Updated `.env.example` with auth settings.
- Updated release/setup checks to include auth files and env keys.
- Updated version to `0.19.0` and frontend asset version to `19`.

---

## Default local login

When the database has no users, the app creates one local admin from `.env` / `.env.example`:

```env
DEFAULT_ADMIN_EMAIL=admin@example.com
DEFAULT_ADMIN_PASSWORD=ChangeMe123!
```

Open the React app and go to:

```text
http://127.0.0.1:5173/#/login
```

Important: change `DEFAULT_ADMIN_PASSWORD` in your local `.env` before using the project beyond local testing. Existing users are not overwritten when you change `.env`.

---

## Fresh clone setup on Windows

After cloning the GitHub repo, run this from the project root:

```bat
setup_windows.bat
```

This will create the virtual environment, install backend requirements, copy `.env.example` to `.env` if missing, create storage folders, initialize SQLite, seed demo data, and install frontend dependencies if npm is available.

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

## Recommended laptop AI settings

Keep Ollama disabled on the laptop until your other desktop is ready:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

The template fallback keeps content package generation working immediately. Provider logs will show disabled providers and the successful fallback.

---

## Auth settings

For local MVP development, this remains safe and flexible:

```env
AUTH_REQUIRED=false
AUTH_TOKEN_TTL_HOURS=72
DEFAULT_ADMIN_EMAIL=admin@example.com
DEFAULT_ADMIN_PASSWORD=ChangeMe123!
```

`AUTH_REQUIRED=false` means older creator routes are still easy to test while the login foundation is being added. User-management APIs still require a `super_admin` login token.

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
28 passed
```

Frontend production build passed after installing frontend dependencies.

---

## Git commands for v19

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
git commit -m "Add role based login foundation"
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
Permission enforcement on sensitive creator actions
```

Recommended commit message for the next step:

```bash
git commit -m "Enforce role permissions on creator workflows"
```
