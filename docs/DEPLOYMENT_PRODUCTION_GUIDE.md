# Deployment Packaging and Production Configuration Guide

This step prepares the MVP for a clean GitHub push, shared ZIP, or simple production-like deployment. The goal is not to over-engineer the app. The goal is to avoid the common mistakes: committing secrets, shipping local databases, exposing dashboards without login, or losing generated data because storage is not persistent.

## What v32 adds

- A deployment guide page in the React app at `#/deployment`.
- Backend deployment guide API endpoints.
- A clean release ZIP builder at `scripts/build_release_package.py`.
- Production-focused `.env.example` keys.
- Release checklist updates for v32.
- Clear commands for tests, frontend build, release package, Git commit, and push.

## Recommended production `.env` overrides

Copy `.env.example` to `.env` on the server and change these values before any public demo or production use:

```env
ENVIRONMENT=production
AUTH_REQUIRED=true
DEFAULT_ADMIN_PASSWORD=replace-with-a-strong-password
AUTH_COOKIE_SECURE=true
CORS_ORIGINS=https://your-frontend-domain.example
DATABASE_PATH=/persistent-storage/app.db
YOUTUBE_API_ENABLED=false
YOUTUBE_DRY_RUN=true
```

Keep `.env` only on your local/server machine. Never commit it.

## Backend deployment

For a simple VPS or Windows server:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/setup_project.py --check-only
python scripts/init_db.py
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For Linux/macOS activation, use:

```bash
source .venv/bin/activate
```

For Render/Railway style hosting:

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Use the hosting dashboard to add environment variables. Do not upload `.env` with secrets.

## Frontend deployment

Build the React app:

```bash
npm run frontend:install
npm run frontend:build
```

The frontend output is created in:

```text
frontend/dist
```

For a separately hosted frontend, set `frontend/.env` or host environment:

```env
VITE_API_BASE_URL=https://your-backend-domain.example
```

Then rebuild the frontend.

## Clean release package

Create a clean ZIP without local databases, secrets, generated exports, OAuth files, virtual environments, node_modules, or frontend build output:

```bash
python scripts/build_release_package.py
```

Default output:

```text
dist_release/edu-content-platform-mvp-v32.zip
```

Preview included files without creating the ZIP:

```bash
python scripts/build_release_package.py --dry-run
```

Create a custom package path:

```bash
python scripts/build_release_package.py --output dist_release/my-release.zip
```

## Final checks before push

```bash
git status
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:install
npm run frontend:build
python scripts/pre_push_check.py
python scripts/build_release_package.py
git status
git add .
git status
git commit -m "Add deployment packaging and production configuration guide"
git push
```

## Do not commit

- `.env`
- `.venv/`
- `frontend/node_modules/`
- `frontend/dist/`
- `storage/app.db`
- generated media and exports under `storage/`
- `storage/youtube_oauth/` secrets/tokens
- `dist_release/`
- logs and cache files

## Backup and rollback

Before updating a deployed app:

1. Stop the backend process.
2. Back up `storage/app.db`.
3. Back up generated package folders if needed.
4. Deploy the new release ZIP.
5. Run health checks.
6. If anything fails, restore the previous ZIP and database backup.

Health checks:

```text
/api/health
/api/system/readiness
```

## Production note

SQLite is acceptable for an MVP demo, but it must be stored on persistent disk. For higher traffic or team usage, migrate to PostgreSQL later.
