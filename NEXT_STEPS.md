# NEXT STEPS — v21

Current version: `0.21.0`

## Completed in this step

- Permission-aware frontend action guards.
- Shared frontend auth context for role-aware UI decisions.
- Reusable `GuardedButton`, `GuardedLink`, and `PermissionNotice` components.
- Locked UI actions for create package, batch, calendar, visual assets, prompt templates, review, source safety, trust review, audio, assembly, video draft, learning outputs, analytics, and demo seed workflows.
- Sidebar navigation now hides role-restricted destinations when strict auth is enabled.
- Role Permissions page now displays current-user allowed/blocked action cards.

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
git commit -m "Add permission aware frontend action guards"
git push
```

## Next build recommendation

Add permission-aware frontend action guards so users can see which actions they cannot perform before clicking.

Next commit message:

```bash
git commit -m "Add permission aware frontend action guards"
```


## v21 completed

- Permission-aware frontend action guards were added.
- UI actions now lock/hide based on role permissions before the backend rejects the request.
- Next recommended step: production auth hardening and route guard polish.

Suggested commit message:

```bash
git commit -m "Add permission aware frontend action guards"
```
