# NEXT STEPS — v20

Current version: `0.20.0`

## Completed in this step

- Permission enforcement foundation for sensitive creator workflows.
- Backend route dependencies for create/edit/review/generate/manage APIs.
- Local permissive mode when `AUTH_REQUIRED=false`.
- Strict role enforcement when `AUTH_REQUIRED=true`.
- Permission matrix API and frontend page.
- Sidebar fix for overflowing navigation links.

## Test now

```bash
python scripts/setup_project.py --check-only
python -m pytest
npm run frontend:build
python scripts/pre_push_check.py
```

Manual UI checks:

```text
1. Open http://127.0.0.1:5173
2. Confirm sidebar scrolls and all links are visible.
3. Open #/permissions.
4. Confirm role/permission matrix loads.
5. Open #/login and login with local admin.
6. Optional: set AUTH_REQUIRED=true and confirm protected actions need login.
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
git commit -m "Enforce role permissions on creator workflows and fix sidebar navigation"
git push
```

## Next build recommendation

Add permission-aware frontend action guards so users can see which actions they cannot perform before clicking.

Next commit message:

```bash
git commit -m "Add permission aware frontend action guards"
```
