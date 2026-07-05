# Next Steps After v12

## What changed in v12

- Added **Notes, quiz, flashcards, and worksheet outputs**.
- Added backend service `learning_output_service.py`.
- Added `learning_outputs` database table.
- Added API endpoints:
  - `POST /api/content/{package_id}/learning-output`
  - `GET /api/content/{package_id}/learning-outputs`
  - `GET /content/{package_id}/learning-output/{output_id}/download`
- Added React package-detail section: **Learning outputs**.
- Export ZIP now includes:
  - `revision_notes.md`
  - `flashcards.json`
  - `quiz_questions.json`
  - `worksheet.md`
  - `learning_outputs.json`
- Added `LEARNING_OUTPUT_DIR=storage/learning_outputs` to `.env.example`.
- Added generated learning output files to `.gitignore`.

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

1. Create/open a package.
2. Generate source safety review.
3. Generate trust review.
4. Click **Generate learning outputs**.
5. Download the learning output pack.
6. Export ZIP and check `revision_notes.md`, `flashcards.json`, `quiz_questions.json`, and `worksheet.md`.

---

## Git commands for this step

Use this commit message exactly for the v12 change:

```bash
git status
git add .
git status
git commit -m "Add notes quiz flashcard and worksheet outputs"
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

## Recommended next feature

Next build: **Prompt Template Manager**.

Reason: after you can create Shorts and learning materials, the next improvement is controlling hook/script/storyboard/title templates from the UI instead of editing code.

Suggested next commit message:

```bash
git commit -m "Add prompt template manager workflow"
```
