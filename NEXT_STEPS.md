# Next Steps After v9

## What changed in v9

- Added **Thumbnail Helper workflow**.
- Added backend service `thumbnail_service.py`.
- Added `thumbnail_guides` database table.
- Added API endpoints:
  - `POST /api/content/{package_id}/thumbnail`
  - `GET /api/content/{package_id}/thumbnails`
  - `GET /content/{package_id}/thumbnail/{guide_id}/download`
- Added React package-detail section: **Thumbnail helper**.
- Export ZIP now includes:
  - `thumbnail_guides.json`
  - `thumbnail_guide.md`
  - `thumbnail_canva_prompt.txt`
  - downloaded thumbnail guide markdown files
- Added `THUMBNAIL_DIR=storage/thumbnails` to `.env.example`.
- Added thumbnail storage to `.gitignore`.

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
2. Review the script and title options.
3. Click **Generate thumbnail helper**.
4. Check thumbnail text ideas, layout guide, and Canva/CapCut prompt.
5. Download the guide or export ZIP.
6. Use `thumbnail_canva_prompt.txt` in Canva/CapCut while creating the thumbnail.

---

## Git commands for this step

Use this commit message exactly for the v9 change:

```bash
git status
git add .
git status
git commit -m "Add thumbnail helper workflow for Shorts packages"
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
__pycache__/
.pytest_cache/
```

---

## Recommended next feature

Next build: **Source Safety + Originality Check**.

Reason: before publishing regularly, every Short should have source/license tracking and a copied-text warning. This protects trust and reduces content risk.

Suggested next commit message:

```bash
git commit -m "Add source safety and originality review workflow"
```
