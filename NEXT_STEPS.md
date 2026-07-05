# Next Steps After v16

## What changed in v16

v16 stabilizes the MVP for daily testing and demos.

Added:

- MVP demo setup screen
- system readiness checks
- demo data seed API
- demo data seed script
- demo Science Shorts batch
- demo packages with analytics, reviews, thumbnails, learning outputs, calendar entries, and provider logs
- safer local test workflow before adding more features

## How to test v16

```bash
python scripts/init_db.py
python scripts/seed_demo_data.py
uvicorn app.main:app --reload
```

Second terminal:

```bash
npm run frontend:install
npm run frontend:dev
```

Then open:

```text
http://127.0.0.1:5173/#/demo
```

Check:

- readiness checklist
- storage folder checks
- provider checks
- demo seed button
- Dashboard demo packages
- Analytics insights demo data
- Provider logs demo data

## Git command for v16

```bash
git status
git add .
git status
git commit -m "Stabilize MVP with demo data and usability fixes"
git push
```

## Next recommended build

Production cleanup and release checklist:

- route-level validation pass
- README screenshot checklist
- `.env.example` cleanup
- one-command dev run notes
- Windows troubleshooting page
- GitHub issue templates
- release checklist before sharing with others

Commit message:

```bash
git commit -m "Add production cleanup and release checklist"
```
