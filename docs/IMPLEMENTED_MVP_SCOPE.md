# Implemented MVP Scope — v7

This build follows the planning document's rule: build tools that help publish better Shorts faster, reduce risk, and save repeated manual time.

## Implemented

- FastAPI backend
- SQLite database
- React/Vite npm frontend
- Legacy Jinja fallback UI
- Concept input form
- Template-based content generator
- AI provider fallback chain
- Script, storyboard, subtitles, visual prompts, titles, description, hashtags, quiz question
- Teacher Trust Score
- Review/edit/approve workflow
- Manual analytics entry
- Content batch planner
- Publishing calendar
- TTS/audio provider chain
  - Windows SAPI provider
  - Optional pyttsx3 provider
  - Manual recording fallback
- Audio asset download
- CapCut/manual assembly plan export
- Simple vertical MP4 draft generation
  - Scene-card video drafts
  - Narration audio merge when WAV exists
  - Silent MP4 fallback when no audio exists
  - Manual video guide fallback when rendering fails
- Export ZIP with content files, subtitles, visual prompts, audio assets/guides, assembly plans, and video drafts
- GitHub-ready `.gitignore`
- Backend tests

## Not implemented yet

- Full curriculum ingestion
- Full knowledge graph
- Real LLM prompt quality tuning
- Ollama desktop deployment
- Piper/Coqui TTS
- Reusable visual asset library
- AI image generation
- Advanced animation engine
- Thumbnail generation
- YouTube API publishing
- Automated analytics sync

## Current recommended use

```text
Plan batch → Generate package → Generate narration/recording guide → Review/edit → Generate assembly plan → Generate MP4 draft → Schedule → Export ZIP → Improve manually → Publish → Enter analytics
```

## Next implementation target

```text
Reusable visual asset library
```

This should allow the draft generator to reuse real icons, diagrams, and backgrounds before any paid or heavy AI image generation is added.
