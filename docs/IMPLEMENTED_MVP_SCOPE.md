# Implemented MVP Scope

This codebase implements the revenue-first Creator Assistant MVP from the planning document.

## Implemented in v3

- FastAPI backend
- SQLite storage
- REST API for npm frontend
- React/Vite frontend
- Legacy Jinja web UI kept as a backup
- Content package form
- Template fallback content generation
- AI provider fallback architecture
  - Ollama provider, disabled by default
  - Transformers provider, disabled by default
  - Template provider, always available
- Provider status page/API
- Shorts script output
- Storyboard output
- Subtitle SRT output
- Visual prompt output
- Title/description/hashtag output
- Quiz question output
- Teacher Trust Score
- Review/edit workflow
- Manual analytics entry
- ZIP export
- `.gitignore` for Python, Node, local databases, generated exports/media, and env files

## Not implemented yet

- Real backend TTS/audio file generation
- Full video assembly
- Content batch planner
- Publishing calendar
- Celery pipeline
- Knowledge graph
- Automated fact verification
- YouTube API integration
- Thumbnail generator
- SEO automation

## Current development rule

Do not build the full platform before using this MVP to create real Shorts packages.

Current vertical slice:

```text
Concept → Script → Storyboard → Subtitles → Review → Export Package → Manual Analytics
```

Next vertical slice:

```text
Content batch planner → TTS/audio fallback → CapCut/manual assembly export → publish 20–30 Shorts → record analytics
```
