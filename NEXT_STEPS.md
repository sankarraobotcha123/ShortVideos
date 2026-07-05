# Next Steps After v13

## What changed in v13

- Added **Prompt Template Manager workflow**.
- Added backend service `prompt_template_service.py`.
- Added `prompt_templates` database table.
- Seeded default script templates:
  - Curiosity Short Script
  - Mistake Correction Script
  - Exam-Focused Script
  - Story / Analogy Script
  - Quick Revision Script
- Added package fields:
  - `prompt_template_id`
  - `prompt_template_name`
  - `prompt_template_style`
  - `prompt_template_snapshot`
- Added API endpoints:
  - `GET /api/prompt-templates`
  - `POST /api/prompt-templates/seed`
  - `POST /api/prompt-templates`
  - `PATCH /api/prompt-templates/{template_id}`
  - `DELETE /api/prompt-templates/{template_id}`
  - `POST /api/prompt-templates/{template_id}/preview`
- Added React screen: **Prompt templates**.
- Added prompt-template selector to Create Package form.
- Export ZIP now includes `prompt_template_snapshot.txt` when a package uses a template.
- Updated frontend asset version to 13.

---

## Immediate test workflow

Backend:

```bash
python -m venv .venv
.venv\Scriptsctivate
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
2. Open **Prompt templates**.
3. Click **Seed default templates** if templates are missing.
4. Create or edit one template.
5. Click **Preview**.
6. Open **Create package**.
7. Select a prompt template.
8. Generate the package.
9. Open package detail and confirm the template name appears under AI provider attempts.
10. Export ZIP and check `prompt_template_snapshot.txt`.

---

## Git commands for this step

Use this commit message exactly for the v13 change:

```bash
git status
git add .
git status
git commit -m "Add prompt template manager workflow"
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
Better Analytics Dashboard Insights
```

Recommended commit message for the next step:

```bash
git commit -m "Add analytics dashboard insights workflow"
```

Why this is next:

- You already have package creation, review, source safety, trust score, learning outputs, thumbnails, batches, calendar, and prompt templates.
- Now the system should help you learn which Shorts, hooks, topics, templates, and batches perform better.
- This supports the business goal: publish consistently, measure, and improve.
