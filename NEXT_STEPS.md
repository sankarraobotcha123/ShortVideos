# Next Steps After v5

## What changed in v5

- TTS/audio fallback system added.
- Windows SAPI provider added for Windows machines where built-in speech works.
- pyttsx3 provider added as optional but disabled by default.
- Manual recording fallback added and always available.
- Package detail page now has a **Generate narration** section.
- Audio files/guides can be downloaded from the frontend.
- Export ZIP now includes audio asset metadata and generated audio/recording guide files.
- Audio fallback status page added.
- API tests now cover audio fallback.
- Tests passed: `6 passed`.

---

## Immediate development plan

### Step 1: Run and test

Backend:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python scripts/init_db.py
uvicorn app.main:app --reload
```

Frontend:

```bash
npm run frontend:install
npm run frontend:dev
```

Open:

```text
http://127.0.0.1:5173
```

---

### Step 2: Test narration fallback

1. Create a content package.
2. Open the package detail page.
3. Click **Generate narration**.
4. If Windows SAPI works, download/play the `.wav` file.
5. If it does not work, download the manual recording guide.

Recommended `.env` for your current laptop:

```env
TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false
```

This keeps publishing possible even if no TTS engine works.

---

### Step 3: Push to GitHub

```bash
git init
git add .
git status
git commit -m "Add audio fallback workflow"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

Make sure these are not committed:

```text
.env
.venv/
frontend/node_modules/
storage/app.db
storage/exports/
storage/audio/
storage/final/
```

---

## Next feature: CapCut/manual assembly export

Before building full automatic video generation, export a creator-friendly assembly package:

```text
script.txt
subtitles.srt
storyboard.md
visual_prompts.md
narration.wav or recording-guide.txt
capcut_scene_plan.md
publish_metadata.md
```

Recommended API:

```text
POST /api/content/{id}/assembly-plan
GET  /content/{id}/export
```

What the assembly plan should contain:

```text
Scene number
Start time
End time
Script segment
Suggested visual
Suggested transition
Subtitle text
Audio instruction
CapCut editing note
```

This is the best next step because it helps you publish Shorts even before full video automation is reliable.

---

## Feature after CapCut export: simple vertical video draft

Only after the package workflow is useful:

```text
MoviePy or FFmpeg
background image/cards + narration + subtitles → vertical 9:16 draft video
```

Keep this simple first:

```text
1. One background per scene
2. Burn subtitles
3. Use narration audio if available
4. Export MP4 draft
```

Do not block publishing on perfect animation automation.

---

## AI provider plan

### Current laptop

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
```

### Later desktop with Ollama

```env
AI_PROVIDER_CHAIN=ollama,transformers,template
USE_OLLAMA=true
OLLAMA_MODEL=llama3.1:8b
```

The provider system already supports this switch.

---

## Build priority reminder

Only build features that help one of these goals:

```text
1. Publish better Shorts faster.
2. Reduce factual/content risk.
3. Understand what the audience likes.
4. Save repeated manual time.
```

Postpone everything else.
