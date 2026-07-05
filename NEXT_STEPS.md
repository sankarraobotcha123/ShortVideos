# NEXT STEPS — v25

Current version: `0.25.0`

## Completed in this step

- Added Content Idea Backlog workflow.
- Added weighted topic scoring for Shorts ideas.
- Added idea statuses: backlog, shortlisted, ready, converted, archived.
- Added idea types: curiosity, textbook doubt, exam friendly, myth vs fact, mistake correction, series.
- Added conversion from a scored idea into a generated content package.
- Added downloadable content idea backlog report.
- Added demo seed support for ideas.

## Test now

```bash
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
```

Manual UI checks:

```text
1. Open http://127.0.0.1:5173/#/ideas.
2. Add a new content idea.
3. Confirm total score and priority appear.
4. Edit score fields and confirm the recommendation changes.
5. Convert an idea to a package.
6. Open the generated package and confirm the topic matches the idea.
7. Download the idea backlog report.
8. Confirm sidebar and dashboard links open the backlog.
```

## Git commands

```bash
git status
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
git status
git add .
git status
git commit -m "Add content idea backlog and topic scoring workflow"
git push
```

## Next build recommendation

Add a **Series Planner workflow** so you can group related Shorts into learning series and playlists before publishing.

Next commit message:

```bash
git commit -m "Add content series planner workflow"
```
