# Next Steps After v3

## What changed in v3

- React/Vite npm frontend added as the main UI.
- FastAPI REST APIs added for dashboard, generation, review, analytics, and AI provider status.
- Jinja pages kept as a backup UI.
- Ollama remains optional and disabled by default.
- Transformers remains optional and disabled by default.
- Template fallback keeps the app working immediately.
- `.gitignore` added for Python, Node, local databases, generated media, cache files, and environment files.

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

### Step 2: Push to GitHub

```bash
git init
git add .
git status
git commit -m "Initial Edu Content Platform MVP"
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

### Step 3: Improve the React UI

Recommended improvements:

- Better mobile layout for content review.
- Add search/filter by topic, subject, status, trust score.
- Add dashboard cards for content targets.
- Add a "copy full publish package" button.
- Add a "duplicate package" button for similar concepts.

---

### Step 4: Add content batch planner

Build this before heavy AI automation.

Useful tables/features:

```text
ContentBatch
- name
- niche
- target_audience
- planned_count
- completed_count
- published_count
- notes

PublishingCalendar
- package_id
- planned_publish_date
- actual_publish_date
- platform
- status
- playlist_name
```

Why this matters:

```text
The business goal is consistent Shorts publishing, not random one-off generation.
```

---

### Step 5: Add TTS/audio fallback

Because Ollama is not available on the laptop, keep AI text generation simple and focus on production helpers.

Fallback order:

```text
1. Browser voice preview now available in React.
2. Add backend text-to-audio using pyttsx3 or edge-tts later.
3. Add Piper/Coqui later if local setup is stable.
4. Allow manual voice recording fallback always.
```

Suggested first backend TTS output:

```text
storage/audio/package-{id}/narration.wav
```

---

### Step 6: Add CapCut/manual assembly export

Before full video generation, export a creator-friendly package:

```text
script.txt
subtitles.srt
storyboard.md
visual_prompts.md
capcut_scene_plan.md
publish_metadata.md
```

This lets publishing continue even while automation is incomplete.

---

### Step 7: Add simple video assembly later

Only after the package workflow is useful:

```text
MoviePy or FFmpeg
images + narration + subtitles → vertical 9:16 draft video
```

Do not block publishing on perfect video automation.

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
