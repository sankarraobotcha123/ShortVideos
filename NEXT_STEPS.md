# Next Steps After v6

## What changed in v6

- Added **CapCut/manual assembly plan** generation.
- Added backend service `assembly_service.py`.
- Added `assembly_plans` database table.
- Added API endpoints:
  - `POST /api/content/{id}/assembly`
  - `GET /api/content/{id}/assembly`
  - `GET /content/{id}/assembly/{plan_id}/download`
- Added React package-detail section: **Generate assembly plan**.
- Export ZIP now includes:
  - `capcut_assembly_plan.md`
  - `assembly_plan.json`
  - `assembly_plans.json`
- Backend tests passed: `7 passed`.
- Frontend production build passed.

---

## Immediate test workflow

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

Test:

1. Create or open a package.
2. Click **Generate narration**.
3. Click **Generate assembly plan**.
4. Download the plan or export the ZIP.
5. Open `capcut_assembly_plan.md` and use it while editing in CapCut.

---

## Git push command

```bash
git add .
git status
git commit -m "Add CapCut assembly planning workflow"
git push
```

Make sure these are not committed:

```text
.env
.venv/
frontend/node_modules/
frontend/dist/
storage/app.db
storage/exports/
storage/audio/
storage/final/
```

---

## Recommended next feature: simple vertical video draft

Now that you have script, subtitles, audio/guide, and CapCut plan, the next feature can be a simple MP4 draft generator.

First version should be basic:

```text
Script + scene plan + generated/manual audio + simple background cards + subtitles → 9:16 MP4 draft
```

Suggested implementation:

- Use MoviePy or FFmpeg.
- Use plain background cards first, not AI images.
- Burn subtitles or display scene text.
- Use narration audio if a WAV exists.
- If no WAV exists, generate a silent draft with timing cards.
- Export to `storage/final/`.

Do not build complex animation yet. The goal is a rough draft that can be improved in CapCut.

---

## Feature after simple MP4 draft

Add a reusable visual asset library:

```text
storage/assets/
  science/
  math/
  icons/
  backgrounds/
```

Then update the assembly/video draft flow to reuse existing visuals before generating new ones.

---

## Current AI/TTS setup reminder

For this laptop:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false

TTS_PROVIDER_CHAIN=windows_sapi,manual_recording
USE_WINDOWS_SAPI_TTS=true
USE_PYTTSX3_TTS=false
```

Later desktop with Ollama:

```env
AI_PROVIDER_CHAIN=ollama,transformers,template
USE_OLLAMA=true
OLLAMA_MODEL=llama3.1:8b
```

---

## Build priority reminder

Only build features that help one of these goals:

```text
1. Publish better Shorts faster.
2. Reduce factual/content risk.
3. Understand what the audience likes.
4. Save repeated manual time.
```
