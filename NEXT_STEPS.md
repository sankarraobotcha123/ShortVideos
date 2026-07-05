# Next Steps After v10

## What changed in v10

- Added **Source Safety + Originality Review workflow**.
- Added backend service `source_safety_service.py`.
- Added `source_safety_reviews` database table.
- Added API endpoints:
  - `POST /api/content/{package_id}/source-safety`
  - `GET /api/content/{package_id}/source-safety`
  - `GET /content/{package_id}/source-safety/{review_id}/download`
- Added React package-detail section: **Source safety & originality**.
- Export ZIP now includes:
  - `source_safety_review.md`
  - `source_safety_checklist.json`
  - `source_safety_reviews.json`
- Added `SOURCE_SAFETY_DIR=storage/source_safety` to `.env.example`.
- Added source safety storage to `.gitignore`.

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

Open:

```text
http://127.0.0.1:5173
```

Test:

1. Create/open a package.
2. Check that source name, license/type, source notes, and transformation notes are filled.
3. Click **Generate source safety review**.
4. Review risk level, similarity score, checklist, and recommendation.
5. If risk is high, rewrite the script and generate another review.
6. Export ZIP and check `source_safety_review.md`.

---

## Git commands for this step

Use this commit message exactly for the v10 change:

```bash
git status
git add .
git status
git commit -m "Add source safety and originality review workflow"
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
__pycache__/
.pytest_cache/
```

---

## Recommended next feature

Next build: **Teacher Trust Score Improvements**.

Reason: source safety tells whether the content is safe/original enough. The next step should make approval stronger by separating trust into factual accuracy, age appropriateness, simplicity, visual clarity, and reviewer confidence.

Suggested next commit message:

```bash
git commit -m "Improve teacher trust score review workflow"
```
