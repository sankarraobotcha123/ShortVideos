# Implemented MVP Scope — v5

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
- Export ZIP with content files, subtitles, visual prompts, and audio assets/guides
- GitHub-ready `.gitignore`
- Backend tests

## Not implemented yet

- Full curriculum ingestion
- Full knowledge graph
- Real LLM prompt quality tuning
- Ollama desktop deployment
- Piper/Coqui TTS
- CapCut scene plan export
- Automatic 9:16 video generation
- Thumbnail generation
- YouTube API publishing
- Automated analytics sync

## Current recommended use

```text
Plan batch → Generate package → Generate narration/recording guide → Review/edit → Schedule → Export ZIP → Assemble manually → Publish → Enter analytics
```

## Next implementation target

```text
CapCut/manual assembly export
```

This should create a scene-by-scene editing plan that can be followed in CapCut before building full video automation.
