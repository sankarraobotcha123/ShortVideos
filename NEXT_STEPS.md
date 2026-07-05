# Next Steps

Current version: `0.32.0`

## Completed in v32

- Added deployment packaging and production configuration guide.
- Added deployment guide page at `#/deployment`.
- Added backend deployment guide endpoints:
  - `GET /api/deployment/guide`
  - `GET /deployment/guide/download`
- Added clean release package builder:
  - `scripts/build_release_package.py`
- Added `docs/DEPLOYMENT_PRODUCTION_GUIDE.md`.
- Added production-focused `.env.example` keys for environment, public URLs, proxy trust, and log level.
- Updated release checklist for v32 packaging and production safety.
- Kept generated media, local databases, OAuth secrets, frontend build output, and release ZIPs protected from Git.

## Recommended next step

**Final MVP bug-fix and UI polish pass**

Suggested commit message:

```bash
git commit -m "Finalize MVP bug fixes and UI polish"
```

## Remaining suggested major steps after v32

1. Final MVP bug-fix and UI polish pass

After v32, there is **1 remaining major step** for the strong MVP roadmap.
