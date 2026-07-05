from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.services.generation_orchestrator import provider_status

COMMIT_MESSAGE = "Add real provider adapter setup guide"

LAPTOP_SAFE_ENV = """AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
USE_HOSTED_LLM=false
""".strip()

OLLAMA_DESKTOP_ENV = """AI_PROVIDER_CHAIN=ollama,transformers,template
USE_OLLAMA=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TIMEOUT_SECONDS=60
USE_TRANSFORMERS=false
USE_HOSTED_LLM=false
""".strip()

TRANSFORMERS_CPU_ENV = """AI_PROVIDER_CHAIN=transformers,template
USE_OLLAMA=false
USE_TRANSFORMERS=true
TRANSFORMERS_MODEL=distilgpt2
TRANSFORMERS_MAX_NEW_TOKENS=220
USE_HOSTED_LLM=false
""".strip()

HOSTED_API_ENV = """AI_PROVIDER_CHAIN=hosted_api,template
USE_OLLAMA=false
USE_TRANSFORMERS=false
USE_HOSTED_LLM=true
HOSTED_LLM_PROVIDER=replace_me
HOSTED_LLM_BASE_URL=https://api.example.com/v1
HOSTED_LLM_MODEL=replace_me
HOSTED_LLM_API_KEY=put_this_only_in_local_env_never_commit
HOSTED_LLM_TIMEOUT_SECONDS=60
""".strip()

PROVIDER_PROFILES = [
    {
        "key": "template",
        "name": "Template fallback",
        "best_for": "Daily laptop development and guaranteed package generation.",
        "risk": "Lowest",
        "install_difficulty": "None",
        "recommended_now": True,
        "notes": "Always keep template last in AI_PROVIDER_CHAIN so publishing is never blocked.",
    },
    {
        "key": "ollama",
        "name": "Ollama local LLM",
        "best_for": "A stronger desktop where you can run local models later.",
        "risk": "Medium: needs RAM/GPU/CPU resources and local model download.",
        "install_difficulty": "Medium",
        "recommended_now": False,
        "notes": "Keep disabled on your current laptop. Enable on the desktop after Ollama is installed and a model is pulled.",
    },
    {
        "key": "transformers",
        "name": "Transformers local model",
        "best_for": "Small offline experiments when you can install torch/transformers.",
        "risk": "Medium/high on low-spec laptops because torch installs can be heavy.",
        "install_difficulty": "Medium to high",
        "recommended_now": False,
        "notes": "Use only when Python environment and disk space are ready. Template fallback remains safer for daily work.",
    },
    {
        "key": "hosted_api",
        "name": "Hosted API adapter placeholder",
        "best_for": "Future quality upgrade when paid API usage is justified by real channel performance.",
        "risk": "Cost and API-key safety risk.",
        "install_difficulty": "Low code setup, but billing/key management required.",
        "recommended_now": False,
        "notes": "Do not commit API keys. Add concrete provider implementation only after the MVP proves value.",
    },
]

TEST_COMMANDS = [
    "python scripts/setup_project.py --check-only",
    "python scripts/run_tests.py",
    "uvicorn app.main:app --reload",
    "Open http://127.0.0.1:5173/#/provider-setup",
    "Open http://127.0.0.1:5173/#/settings/ai",
    "Create one test package and check the provider attempt log",
]

GIT_COMMANDS = [
    "git status",
    "python scripts/setup_project.py --check-only",
    "python scripts/run_tests.py",
    "npm run frontend:build",
    "python scripts/pre_push_check.py",
    "git status",
    "git add .",
    "git status",
    f'git commit -m "{COMMIT_MESSAGE}"',
    "git push",
]


def _hosted_status() -> dict[str, Any]:
    enabled = settings.use_hosted_llm
    missing_key = enabled and not settings.hosted_llm_api_key
    if not enabled:
        message = "USE_HOSTED_LLM=false. Hosted APIs are intentionally disabled for the MVP."
        available = False
    elif missing_key:
        message = "USE_HOSTED_LLM=true but HOSTED_LLM_API_KEY is missing in local .env."
        available = False
    else:
        message = "Hosted API settings are present, but concrete hosted adapter implementation is still a future step."
        available = False
    return {
        "name": "hosted_api",
        "available": available,
        "in_chain": "hosted_api" in settings.ai_provider_chain,
        "message": message,
    }


def _read_env_example(project_root: Path) -> str:
    try:
        return (project_root / ".env.example").read_text(encoding="utf-8")
    except Exception:
        return ""


def _env_key_status(project_root: Path) -> list[dict[str, str]]:
    env_text = _read_env_example(project_root)
    keys = [
        "AI_PROVIDER_CHAIN",
        "USE_OLLAMA",
        "OLLAMA_BASE_URL",
        "OLLAMA_MODEL",
        "USE_TRANSFORMERS",
        "TRANSFORMERS_MODEL",
        "USE_HOSTED_LLM",
        "HOSTED_LLM_PROVIDER",
        "HOSTED_LLM_API_KEY",
        "HOSTED_LLM_MODEL",
    ]
    checks = []
    for key in keys:
        found = any(line.strip().startswith(f"{key}=") for line in env_text.splitlines())
        checks.append({
            "key": key,
            "status": "pass" if found else "warn",
            "detail": "Present in .env.example" if found else "Missing from .env.example",
        })
    return checks


def build_provider_setup_guide(project_root: str | Path = ".") -> dict[str, Any]:
    root = Path(project_root).resolve()
    current_status = provider_status()
    current_status.append(_hosted_status())
    env_checks = _env_key_status(root)
    pass_count = sum(1 for item in env_checks if item["status"] == "pass")
    warn_count = sum(1 for item in env_checks if item["status"] != "pass")

    env_profiles = [
        {
            "key": "laptop_safe",
            "title": "Laptop-safe MVP mode",
            "recommended_for": "Your current laptop while Ollama is not working.",
            "env": LAPTOP_SAFE_ENV,
            "when_to_use": "Use this for normal daily development. It always falls back to template generation.",
        },
        {
            "key": "ollama_desktop",
            "title": "Ollama desktop mode",
            "recommended_for": "A stronger desktop where Ollama works.",
            "env": OLLAMA_DESKTOP_ENV,
            "when_to_use": "Use after installing Ollama and confirming the model responds locally.",
        },
        {
            "key": "transformers_local",
            "title": "Transformers local experiment mode",
            "recommended_for": "Offline model experiments when torch/transformers can be installed successfully.",
            "env": TRANSFORMERS_CPU_ENV,
            "when_to_use": "Use only for experiments; do not block publishing on this provider.",
        },
        {
            "key": "hosted_api_future",
            "title": "Hosted API future adapter mode",
            "recommended_for": "Future paid quality upgrade after the channel workflow proves value.",
            "env": HOSTED_API_ENV,
            "when_to_use": "Use later with a real provider adapter. Never commit API keys.",
        },
    ]

    markdown = build_provider_setup_markdown(
        current_status=current_status,
        env_profiles=env_profiles,
        env_checks=env_checks,
    )

    return {
        "summary": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "recommended_current_mode": "Laptop-safe MVP mode",
            "remaining_provider_steps": 3,
            "env_checks_passed": pass_count,
            "env_checks_warnings": warn_count,
            "commit_message": COMMIT_MESSAGE,
        },
        "provider_profiles": PROVIDER_PROFILES,
        "current_status": current_status,
        "env_profiles": env_profiles,
        "env_checks": env_checks,
        "test_commands": TEST_COMMANDS,
        "git_commands": GIT_COMMANDS,
        "guide_markdown": markdown,
    }


def build_provider_setup_markdown(
    *,
    current_status: list[dict[str, Any]],
    env_profiles: list[dict[str, str]],
    env_checks: list[dict[str, str]],
) -> str:
    lines = [
        "# Real Provider Adapter Setup Guide",
        "",
        "This guide keeps the current laptop safe while preparing the project for stronger providers later.",
        "The template provider must always remain as the final fallback so content creation never stops.",
        "",
        "## Current provider status",
        "",
        "| Provider | In chain | Available | Status |",
        "|---|---:|---:|---|",
    ]
    for item in current_status:
        lines.append(
            f"| {item.get('name')} | {'yes' if item.get('in_chain') else 'no'} | {'yes' if item.get('available') else 'no'} | {item.get('message', '')} |"
        )

    lines.extend([
        "",
        "## Recommended order",
        "",
        "1. Keep laptop-safe template fallback for daily publishing.",
        "2. Test Ollama only on the stronger desktop.",
        "3. Try Transformers only if Python/torch installation is stable.",
        "4. Add hosted APIs only after the content workflow proves value and cost is justified.",
        "",
        "## Environment profiles",
        "",
    ])
    for profile in env_profiles:
        lines.extend([
            f"### {profile['title']}",
            "",
            profile["when_to_use"],
            "",
            "```env",
            profile["env"],
            "```",
            "",
        ])

    lines.extend([
        "## .env.example checks",
        "",
        "| Key | Status | Detail |",
        "|---|---|---|",
    ])
    for item in env_checks:
        lines.append(f"| {item['key']} | {item['status']} | {item['detail']} |")

    lines.extend([
        "",
        "## Test commands",
        "",
        "```bash",
        *TEST_COMMANDS,
        "```",
        "",
        "## Git commands",
        "",
        "```bash",
        *GIT_COMMANDS,
        "```",
        "",
        "## Safety rules",
        "",
        "- Do not commit `.env` or API keys.",
        "- Do not remove `template` from the provider chain.",
        "- Do not make Ollama or Transformers mandatory for local MVP development.",
        "- Check provider logs after every test package.",
        "- Add paid/hosted providers only after you know which Shorts format works.",
    ])
    return "\n".join(lines)
