# Next Steps — v18

Current version: `0.18.0`

## Completed in v18

Fresh-clone setup automation.

Added:

- `scripts/setup_project.py`
- `setup_windows.bat`
- `setup_windows.ps1`
- `docs/FRESH_CLONE_SETUP.md`
- Setup guide service
- `/api/setup/guide`
- `/setup/guide/download`
- React Fresh clone setup page at `#/setup`
- Release checklist updated to include setup files
- Version updated to `0.18.0`

## Git commands for this step

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
git commit -m "Add fresh clone setup automation"
git push
```

## Check before committing

Make sure these are not staged:

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

## Next recommended build

**Role-based login foundation**

Suggested commit message:

```bash
git commit -m "Add role based login foundation"
```

Why next: before you turn this into a more serious side-job tool, you should protect admin screens and prepare roles like Super Admin, Content Admin, Script Reviewer, Video Editor, and Publisher.
