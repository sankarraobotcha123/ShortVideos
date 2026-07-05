# Production Cleanup and Release Checklist

Use this checklist before pushing code to GitHub or sharing a project zip.

## Required local checks

```bash
python scripts/init_db.py
python scripts/seed_demo_data.py
python scripts/run_tests.py
npm run frontend:build
python scripts/pre_push_check.py
git status
```

## Git commit message for this step

```bash
git commit -m "Add fresh clone setup automation"
```

## Do not commit generated/local files

Keep these out of Git:

- `.env`
- `.venv/`
- `frontend/node_modules/`
- `frontend/dist/`
- `storage/app.db`
- `storage/exports/`
- `storage/audio/`
- `storage/video_drafts/`
- `storage/asset_library/`
- `storage/thumbnails/`
- `storage/source_safety/`
- `storage/trust_reviews/`
- `storage/learning_outputs/`
- `__pycache__/`
- `.pytest_cache/`

## Release flow

1. Pull latest changes from GitHub.
2. Run backend tests.
3. Run frontend build.
4. Run pre-push check.
5. Check `git status`.
6. Stage files.
7. Check `git status` again.
8. Commit with a clear message.
9. Push.
10. Test the fresh clone/run instructions when possible.


## v18 note

The release checklist now also verifies fresh-clone setup files: `scripts/setup_project.py`, `setup_windows.bat`, `setup_windows.ps1`, and `docs/FRESH_CLONE_SETUP.md`.
