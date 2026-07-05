# Project Audit v34

This audit was added after checking the uploaded laptop project folder that had already been pushed to Git.

## What was checked

- Backend setup check using `python scripts/setup_project.py --check-only`.
- Backend tests using the stable wrapper `python scripts/run_tests.py`.
- Release/pre-push checklist using `python scripts/pre_push_check.py`.
- Clean release package creation using `python scripts/build_release_package.py`.
- Frontend build command availability using `npm run frontend:build`.

## Result

- Backend tests passed.
- Pre-push checklist passed.
- Clean release ZIP creation passed.
- Frontend build could not be completed in the audit sandbox because `frontend/node_modules` is not included in the ZIP. This is expected because `node_modules` should not be committed. Run `npm run frontend:install` before `npm run frontend:build` on the laptop.

## Added improvements

### Stable test runner

Use:

```bash
python scripts/run_tests.py
```

This wrapper disables auto-loading of unrelated global pytest plugins. It keeps test behavior more stable across different laptops, Python installs, IDEs, and CI environments.

### Local cleanup helper

Preview cleanup:

```bash
python scripts/clean_local_artifacts.py
```

Apply cleanup:

```bash
python scripts/clean_local_artifacts.py --apply
```

The helper removes local cache/build artifacts such as `__pycache__`, `.pytest_cache`, `frontend/dist`, and `dist_release`. It does not remove your `.env`, local database, uploaded files, or generated content storage.

## Final push flow

```bash
git status
python scripts/setup_project.py --check-only
python scripts/run_tests.py
npm run frontend:install
npm run frontend:build
python scripts/pre_push_check.py
python scripts/build_release_package.py
git status
git add .
git status
git commit -m "Add final project audit and test stability tools"
git push
```
