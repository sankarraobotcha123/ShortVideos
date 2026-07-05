# YouTube Manual Publishing Checklist

This workflow keeps publishing manual for the MVP while preparing safe placeholders for a future YouTube API adapter.
No automatic YouTube upload is implemented in this step.

## Summary

- Packages checked: 0
- Ready to upload: 0
- Needs publishing gate: 0
- Scheduled: 0
- Published: 0
- API enabled: False
- API dry-run: True

## Manual publishing phases

### Final package review

Confirm the Short is safe, useful, and ready before opening YouTube Studio.

- Review script, subtitles, title options, description, hashtags, and quiz question.
- Confirm source safety review and teacher trust review are complete.
- Confirm publishing approval gate is approved before marking anything as published.
- Check final video duration, spelling, audio clarity, and visual readability on mobile size.

### Export and asset readiness

Prepare upload files and copy blocks without searching inside the project again.

- Export the package ZIP and keep README, subtitle file, script, visual prompts, and video draft together.
- Open the MP4/video draft or editor-exported final video and watch it fully once.
- Prepare the thumbnail manually in Canva/CapCut if a thumbnail guide exists.
- Copy one final title, description, and hashtag set into a publishing note.

### YouTube Studio manual upload

Publish safely without API risk while the MVP is still being validated.

- Upload the final MP4 in YouTube Studio, not through API automation yet.
- Paste the selected title, description, hashtags, playlist, and language metadata.
- Choose the correct audience and visibility settings manually after reviewing the video.
- Keep visibility private/unlisted first if you want one final mobile preview before public release.

### After publishing

Keep the app database aligned with the real channel state.

- Copy the YouTube video URL into the package/calendar notes.
- Update the calendar actual publish date and status.
- Mark the package as published only after the real upload is live.
- Enter manual analytics after enough views are collected so future topics can improve.

## Package readiness

| ID | Title | Review | Gate | Calendar | Readiness | Next action |
|---:|---|---|---|---|---|---|
| - | No packages yet | - | - | - | - | Create and approve one package first. |

## Optional YouTube API preparation

### 1. Keep API mode disabled during MVP validation

Manual publishing is safer until title style, video format, upload cadence, and review gates are stable.

Action: Use YOUTUBE_API_ENABLED=false and YOUTUBE_DRY_RUN=true.

### 2. Prepare OAuth files outside Git

Client secrets and token files belong only in local storage/youtube_oauth and must stay ignored by Git.

Action: Create the files locally later; never place real secrets in docs, commits, or screenshots.

### 3. Add an upload adapter behind a one-method interface

Future code should receive a validated package and return dry-run/upload results without changing business logic.

Action: Implement only after manual publishing proves the workflow.

### 4. Dry-run before any real upload

The first API version should validate title, description, tags, file path, privacy status, and playlist without uploading.

Action: Keep YOUTUBE_DRY_RUN=true until you intentionally test on a private video.

## Environment profiles

### Manual publishing safe mode

Use this now. It avoids OAuth/API upload risk and keeps the workflow manual.

```env
YOUTUBE_API_ENABLED=false
YOUTUBE_DRY_RUN=true
YOUTUBE_OAUTH_DIR=storage/youtube_oauth
YOUTUBE_CLIENT_SECRETS_FILE=storage/youtube_oauth/client_secret.json
YOUTUBE_TOKEN_FILE=storage/youtube_oauth/token.json
YOUTUBE_CHANNEL_ID=
YOUTUBE_DEFAULT_PRIVACY_STATUS=private
YOUTUBE_DEFAULT_PLAYLIST_ID=
YOUTUBE_NOTIFY_SUBSCRIBERS=false
```

### Optional API dry-run preparation

Use later only for dry-run validation first. Do not upload automatically in this MVP step.

```env
YOUTUBE_API_ENABLED=true
YOUTUBE_DRY_RUN=true
YOUTUBE_OAUTH_DIR=storage/youtube_oauth
YOUTUBE_CLIENT_SECRETS_FILE=storage/youtube_oauth/client_secret.json
YOUTUBE_TOKEN_FILE=storage/youtube_oauth/token.json
YOUTUBE_CHANNEL_ID=replace_after_channel_verification
YOUTUBE_DEFAULT_PRIVACY_STATUS=private
YOUTUBE_DEFAULT_PLAYLIST_ID=optional_playlist_id
YOUTUBE_NOTIFY_SUBSCRIBERS=false
```

## .env.example YouTube keys

| Key | Status | Detail |
|---|---|---|
| YOUTUBE_API_ENABLED | pass | Present in .env.example |
| YOUTUBE_DRY_RUN | pass | Present in .env.example |
| YOUTUBE_OAUTH_DIR | pass | Present in .env.example |
| YOUTUBE_CLIENT_SECRETS_FILE | pass | Present in .env.example |
| YOUTUBE_TOKEN_FILE | pass | Present in .env.example |
| YOUTUBE_CHANNEL_ID | pass | Present in .env.example |
| YOUTUBE_DEFAULT_PRIVACY_STATUS | pass | Present in .env.example |
| YOUTUBE_DEFAULT_PLAYLIST_ID | pass | Present in .env.example |
| YOUTUBE_NOTIFY_SUBSCRIBERS | pass | Present in .env.example |

## API safety boundaries

- No automatic upload is implemented in this step.
- No YouTube OAuth secrets, refresh tokens, or API keys are committed.
- Manual review and publishing approval remain required before upload.
- Future API mode should default to private visibility and dry-run validation.
- Analytics sync is still manual until the MVP content format proves useful.

## Test commands

```bash
python scripts/setup_project.py --check-only
python scripts/run_tests.py
npm run frontend:build
uvicorn app.main:app --reload
Open http://127.0.0.1:5173/#/youtube-publishing
Download the checklist and use it for one manually uploaded Short
```

## Git commands

```bash
git status
python scripts/setup_project.py --check-only
python scripts/run_tests.py
npm run frontend:build
python scripts/pre_push_check.py
git status
git add .
git status
git commit -m "Add YouTube publishing checklist workflow"
git push
```
