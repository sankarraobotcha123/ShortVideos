# NEXT STEPS — v22

Current version: `0.22.0`

## Completed in this step

- Production auth hardening checks.
- Super-admin Auth hardening page.
- Expired-session cleanup endpoint.
- Active-session limit enforcement.
- Password rotation endpoint that revokes active sessions.
- Frontend route guards for protected pages.
- Stale-token cleanup after `401` API responses.
- Auth cookie settings for HTTPS-ready deployment.
- Permission protection on generated artifact download/export routes.

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
2. Login as admin@example.com / ChangeMe123!
3. Open #/auth-hardening.
4. Confirm warnings/checklist appear.
5. Change the password and confirm you are redirected to login.
6. Login again with the new password.
7. Optional: set AUTH_REQUIRED=true and restart backend.
8. Open restricted pages directly by URL and confirm route guards show login/permission messages.
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
git commit -m "Harden auth flow and frontend route guards"
git push
```

## Next build recommendation

Add final publishing approval gates so the system helps avoid exporting/publishing a Short before it has passed review, source safety, and trust checks.

Next commit message:

```bash
git commit -m "Add publishing approval gate workflow"
```
