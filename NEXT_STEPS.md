# Next Steps — v19

Current version: `0.19.0`

## Completed in v19

Role-based login foundation.

Added:

- `app/routes/auth.py`
- `app/services/auth_service.py`
- `user_accounts` database table
- `auth_sessions` database table
- Default local admin bootstrap
- PBKDF2-SHA256 password hashing
- Bearer token login sessions
- Login/logout/me/status API routes
- Super-admin user management API routes
- React `#/login` page
- React `#/users` page
- Auth token storage and API headers in `frontend/src/api.js`
- Auth settings in `.env.example`
- Release/setup checks updated for auth files
- Version updated to `0.19.0`

## Test login

Default local account after a new database is created:

```text
Email   : admin@example.com
Password: ChangeMe123!
```

Open:

```text
http://127.0.0.1:5173/#/login
```

Change the password in your local `.env` before using the project beyond local testing.

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
git commit -m "Add role based login foundation"
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

**Permission enforcement on sensitive creator actions**

Suggested commit message:

```bash
git commit -m "Enforce role permissions on creator workflows"
```

Why next: login exists now. The next step should connect roles to sensitive actions like package creation, review approval, publishing calendar changes, asset uploads, prompt-template edits, and exports.
