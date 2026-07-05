# NEXT STEPS — v23

Current version: `0.24.0`

## Completed in this step

- Fixed Prompt templates page crash caused by missing `initialPromptTemplate`.
- Added Publishing Approval Gate workflow.
- Added required publishing checks: script approval, source safety review, source risk, Teacher Trust Score review, and trust score readiness.
- Added optional readiness checks: thumbnail, assembly plan, narration, video draft, learning outputs, and calendar scheduling.
- Added publisher decision controls.
- Blocked `published` status until a publishing gate has been approved.
- Included publishing approval files in exported ZIP packages.

## Test now

```bash
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
```

Manual UI checks:

```text
1. Open http://127.0.0.1:5173/#/templates.
2. Confirm Prompt templates opens without a blank page/error.
3. Create/open a package.
4. Run source safety review.
5. Run Teacher Trust Score review.
6. Save script review as approved.
7. Generate publishing approval gate.
8. Save publisher decision as approved when required checks pass.
9. Confirm Export publish ZIP appears after approval.
10. Try marking a package as published before gate approval and confirm it is blocked.
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
git commit -m "Add content production board workflow"
git push
```

## Next build recommendation

Add a content production board to make daily work easier. It should show packages by workflow status and make it obvious what action is needed next.

Next commit message:

```bash
git commit -m "Add content production board workflow"
```


## Completed in v24 — Content Production Board

Added a Kanban-style production board to track Shorts from script review through publishing and analytics. The board supports manual stage overrides, priority, owner, due dates, notes, and a downloadable markdown board report.

Git commit for this step:

```bash
git commit -m "Add content production board workflow"
```

## Recommended next step

Add a content idea backlog and topic scoring workflow.

Suggested commit message:

```bash
git commit -m "Add content idea backlog and topic scoring workflow"
```
