# Real Provider Adapter Setup Guide

This project should continue working on a normal laptop even when Ollama, Transformers, or paid APIs are unavailable. The safest provider order is:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
USE_HOSTED_LLM=false
```

The `template` provider must stay as the final fallback. It lets you keep producing Shorts packages even when every AI provider fails.

## Recommended provider rollout

1. **Template fallback now** — daily content workflow, guaranteed generation, no setup risk.
2. **Ollama on stronger desktop later** — better script generation without paid APIs.
3. **Transformers local experiments later** — useful for offline tests, but Python/torch setup can be heavy.
4. **Hosted APIs only after validation** — use paid APIs only after the channel workflow proves value.

## Laptop-safe mode

Use this on the current laptop:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
USE_HOSTED_LLM=false
```

## Ollama desktop mode

Use this only after installing Ollama on a stronger desktop and confirming a model works:

```env
AI_PROVIDER_CHAIN=ollama,transformers,template
USE_OLLAMA=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TIMEOUT_SECONDS=60
USE_TRANSFORMERS=false
USE_HOSTED_LLM=false
```

Validation steps:

```bash
uvicorn app.main:app --reload
npm run frontend:dev
```

Then open:

```text
http://127.0.0.1:5173/#/provider-setup
http://127.0.0.1:5173/#/settings/ai
http://127.0.0.1:5173/#/provider-logs
```

Generate one test package and check that provider logs show whether Ollama succeeded or fell back safely.

## Transformers local experiment mode

Use only when you are ready to install heavy dependencies:

```env
AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=true
TRANSFORMERS_MODEL=distilgpt2
TRANSFORMERS_MAX_NEW_TOKENS=220
USE_HOSTED_LLM=false
```

Keep this optional. Do not block publishing on Transformers.

## Hosted API future mode

Use only after the workflow proves value and cost is justified:

```env
AI_PROVIDER_CHAIN=hosted_api,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
USE_HOSTED_LLM=true
HOSTED_LLM_PROVIDER=replace_me
HOSTED_LLM_BASE_URL=https://api.example.com/v1
HOSTED_LLM_MODEL=replace_me
HOSTED_LLM_API_KEY=put_this_only_in_local_env_never_commit
HOSTED_LLM_TIMEOUT_SECONDS=60
```

Rules:

- Never commit `.env`.
- Never commit API keys.
- Keep `template` as fallback.
- Add billing/cost guardrails before enabling hosted APIs.
- Log every provider attempt.

## Test checklist

```bash
python scripts/setup_project.py --check-only
python scripts/run_tests.py
npm run frontend:build
python scripts/pre_push_check.py
```

## Suggested commit message

```bash
git commit -m "Add real provider adapter setup guide"
```
