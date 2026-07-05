# Next Steps After v8

## What changed in v8

- Added **Reusable Visual Asset Library**.
- Added backend service `asset_library_service.py`.
- Added `visual_assets` database table.
- Added API endpoints:
  - `GET /api/assets`
  - `POST /api/assets`
  - `DELETE /api/assets/{asset_id}`
  - `GET /assets/{asset_id}/download`
- Added React screen: **Visual assets**.
- Added suggested visual assets to package detail page.
- Updated MP4 draft generation to use matching uploaded visual assets inside scene cards.
- Export ZIP now includes:
  - `visual_assets.json`
  - copies of saved visual asset files inside `visual_assets/`
- Backend tests passed: `9 passed`.
- Frontend production build passed.

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

1. Go to **Visual assets**.
2. Upload a leaf/chlorophyll image.
3. Add tags: `leaf, chlorophyll, photosynthesis, science`.
4. Create/open a package: `Why are leaves green?`.
5. Check **Suggested reusable visuals**.
6. Generate video draft.
7. Confirm the scene card uses the uploaded asset when matched.
8. Export ZIP.

---

## Git push command

```bash
git add .
git status
git commit -m "Add reusable visual asset library"
git push
```

Make sure these are not committed:

```text
.env
.venv/
frontend/node_modules/
frontend/dist/
storage/app.db
storage/exports/
storage/audio/
storage/video_drafts/
storage/asset_library/*
storage/final/
```

---

## Recommended next feature: thumbnail helper

The next best feature is **thumbnail helper**, not full thumbnail prediction.

First version should generate:

```text
Topic + hook + title options → thumbnail text ideas + layout guide + Canva/CapCut prompt
```

Suggested output:

```text
1. Thumbnail text option
2. Emotion/curiosity angle
3. Visual layout
4. Background idea
5. Main object/image suggestion
6. Color/contrast note
7. What not to put on thumbnail
```

Why this is next:

- It directly helps Shorts/YouTube packaging.
- It does not require paid image generation.
- It improves click interest while the content workflow is still manual-first.

---

## Feature after thumbnail helper

Add **basic notes + quiz worksheet export**:

```text
Approved script → short notes → 5-question quiz → worksheet markdown/PDF-ready export
```

This supports future monetization through PDFs, worksheets, and study packs.
