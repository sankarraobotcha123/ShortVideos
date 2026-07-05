# Next Steps After v11

## What changed in v11

- Added **Teacher Trust Score Review workflow**.
- Added backend service `trust_score_service.py`.
- Added `teacher_trust_reviews` database table.
- Added API endpoints:
  - `POST /api/content/{package_id}/trust-review`
  - `GET /api/content/{package_id}/trust-reviews`
  - `PATCH /api/content/{package_id}/trust-review/{review_id}`
  - `GET /content/{package_id}/trust-review/{review_id}/download`
- Added React package-detail section: **Teacher Trust Score review**.
- Added editable category scores:
  - Factual accuracy
  - Age appropriateness
  - Simplicity
  - Visual clarity
  - Engagement
  - Source safety
  - Reviewer confidence
- Export ZIP now includes:
  - `teacher_trust_review.md`
  - `teacher_trust_checklist.json`
  - `teacher_trust_reviews.json`
- Added `TRUST_REVIEW_DIR=storage/trust_reviews` to `.env.example`.
- Added trust review generated files to `.gitignore`.

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
2. Click **Generate source safety review**.
3. Click **Generate trust review**.
4. Edit category scores.
5. Add reviewer notes.
6. Set reviewer decision to `approved` or `edit_required`.
7. Save trust review.
8. Export ZIP and check `teacher_trust_review.md`.

---

## Git commands for this step

Use this commit message exactly for the v11 change:

```bash
git status
git add .
git status
git commit -m "Improve teacher trust score review workflow"
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
__pycache__/
.pytest_cache/
```

---

## Recommended next feature

Next build: **Notes, quiz, flashcards, and worksheet outputs**.

Reason: once Shorts packages have safety and trust checks, the same content should produce reusable learning products that can later become PDFs, quizzes, worksheets, mini-courses, or paid packs.

Suggested next commit message:

```bash
git commit -m "Add notes quiz flashcard and worksheet outputs"
```
