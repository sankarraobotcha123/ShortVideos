# Next Steps After v15

## What changed in v15

- Added **AI Provider Fallback Logging workflow**.
- Added backend service `provider_log_service.py`.
- Added database table `ai_provider_logs`.
- Added timing metadata to provider attempts.
- Added API endpoint:
  - `GET /api/provider-logs`
- Package generation now stores provider attempts as queryable log rows.
- Package detail API now returns `provider_logs`.
- Export ZIP now includes:
  - `ai_provider_logs.json`
  - `ai_provider_log_report.md`
- Added React screen: **Provider logs**.
- Added sidebar navigation for Provider logs.
- Added package-detail **AI provider attempt log** section.
- Added dashboard quick action to review provider logs.
- Updated frontend asset version to 15.

---

## Immediate test workflow

Backend:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

Frontend:

```bash
npm run frontend:install
npm run frontend:dev
```

Test:

1. Open `http://127.0.0.1:5173`.
2. Create a content package.
3. Open the package detail page.
4. Check **AI provider attempt log**.
5. Open **Provider logs** from the sidebar.
6. Confirm provider successes/failures and recommendations.
7. Export the package ZIP.
8. Confirm `ai_provider_logs.json` and `ai_provider_log_report.md` are present.

---

## Git commands for this step

Use this commit message exactly for the v15 change:

```bash
git status
git add .
git status
git commit -m "Improve AI provider fallback logging workflow"
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
__pycache__/
.pytest_cache/
```

---

## Next recommended step

Next build should be:

```text
MVP Stabilization and Demo Data Seed Workflow
```

Why this is next:

- The main Shorts workflow is now broad enough for daily use.
- Before adding more large features, the project needs better demo data, smoother empty states, safer validation, and a clear test/demo setup.
- This will make it easier to push to GitHub, demo the project, and continue development without confusion.

Recommended commit message for the next step:

```bash
git commit -m "Stabilize MVP with demo data and usability fixes"
```
