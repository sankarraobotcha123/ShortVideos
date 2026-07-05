# Next Steps After v7

## What changed in v7

- Added **simple vertical MP4 draft generation**.
- Added backend service `video_draft_service.py`.
- Added `video_drafts` database table.
- Added API endpoints:
  - `POST /api/content/{id}/video-draft`
  - `GET /api/content/{id}/video-drafts`
  - `GET /content/{id}/video-draft/{draft_id}/download`
- Added React package-detail section: **Generate video draft**.
- Export ZIP now includes:
  - generated MP4 draft or manual guide file
  - `video_drafts.json`
- Backend tests passed: `8 passed`.
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

1. Create or open a package.
2. Click **Generate narration**.
3. Click **Generate assembly plan**.
4. Click **Generate video draft**.
5. Preview/download the MP4 draft.
6. Export the ZIP.
7. Improve the MP4 manually in CapCut if needed.

---

## Git push command

```bash
git add .
git status
git commit -m "Add vertical MP4 draft generator"
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
storage/final/
```

---

## Recommended next feature: reusable visual asset library

Now that the app can generate script, audio/guide, CapCut plan, and a simple video draft, the next best feature is reusable visual assets.

First version should be simple:

```text
Asset upload/import → tag asset → choose asset during draft generation → reuse before creating new visuals
```

Suggested folders:

```text
storage/asset_library/
  science/
  math/
  icons/
  backgrounds/
  diagrams/
```

Suggested database table:

```text
AssetLibraryItem
  id
  tag
  topic_area
  file_path
  file_name
  asset_type
  reuse_count
  notes
```

Update the video draft generator to prefer:

```text
Matching reusable asset → generated scene card fallback
```

This improves quality without needing paid image generation.

---

## Feature after asset library

Add a simple **thumbnail helper**:

```text
Topic + hook + title → thumbnail text ideas + layout guide + export prompt
```

Do not build a full thumbnail prediction engine yet. Generate useful thumbnail guidance first.
