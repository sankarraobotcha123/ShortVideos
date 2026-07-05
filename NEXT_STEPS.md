# Next Steps After v14

## What changed in v14

- Added **Analytics Dashboard Insights workflow**.
- Added backend service `analytics_insights_service.py`.
- Added API endpoint:
  - `GET /api/analytics/insights`
- Added React screen: **Analytics insights**.
- Added sidebar navigation for Analytics insights.
- Added dashboard quick action to open analytics insights.
- Added analytics insight calculations:
  - total latest views
  - average retention
  - average CTR
  - engagement rate
  - top videos by views
  - top videos by retention
  - weak videos to improve
  - tone performance
  - prompt-template performance
  - subject performance
  - batch performance
  - weekly summary
  - recommendations
  - downloadable markdown report from the browser
- Updated frontend asset version to 14.

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
2. Create at least 3 packages.
3. Open each package and add manual analytics.
4. Open **Analytics insights** from the sidebar.
5. Check top videos, weak videos, tone/template/batch performance, and weekly summary.
6. Click **Download report** and confirm `analytics_dashboard_insights.md` downloads.

---

## Git commands for this step

Use this commit message exactly for the v14 change:

```bash
git status
git add .
git status
git commit -m "Add analytics dashboard insights workflow"
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
AI Provider Fallback Logging Improvements
```

Why this is next:

- You are not using Ollama on the laptop now.
- The project already supports fallback generation, but logging can be clearer.
- Better provider logs will help you safely test template, Transformers, and later Ollama on another desktop.
- This keeps the project ready for better AI without breaking the current workflow.

Recommended commit message for the next step:

```bash
git commit -m "Improve AI provider fallback logging workflow"
```
