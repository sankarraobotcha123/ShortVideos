from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COMMIT_MESSAGE = "Add real provider adapter setup guide"

WINDOWS_SETUP_COMMANDS = [
    "git clone YOUR_GITHUB_REPO_URL short_videos",
    "cd short_videos",
    "py -3.12 -m venv .venv",
    r".venv\\Scripts\\activate",
    "python -m pip install --upgrade pip",
    "pip install -r requirements.txt",
    "copy .env.example .env",
    "python scripts/setup_project.py --seed-demo",
    "npm run frontend:install",
    "uvicorn app.main:app --reload",
]

FRONTEND_COMMANDS = [
    "npm run frontend:install",
    "npm run frontend:dev",
]

BACKEND_COMMANDS = [
    r".venv\\Scripts\\activate",
    "uvicorn app.main:app --reload",
]

GIT_COMMANDS = [
    "git status",
    "python scripts/setup_project.py --check-only",
    "python -m pytest",
    "npm run frontend:build",
    "python scripts/pre_push_check.py",
    "git status",
    "git add .",
    "git status",
    f'git commit -m "{COMMIT_MESSAGE}"',
    "git push",
]

REQUIRED_SETUP_FILES = [
    "scripts/setup_project.py",
    "setup_windows.bat",
    "setup_windows.ps1",
    "docs/FRESH_CLONE_SETUP.md",
    "docs/PROVIDER_ADAPTER_SETUP.md",
    ".env.example",
    "requirements.txt",
    "package.json",
    "frontend/package.json",
    "app/routes/auth.py",
    "app/services/auth_service.py",
]

SETUP_STEPS = [
    {
        "step": 1,
        "title": "Clone the repository",
        "description": "Download the code from GitHub to a clean folder.",
        "command": "git clone YOUR_GITHUB_REPO_URL short_videos",
    },
    {
        "step": 2,
        "title": "Create and activate virtual environment",
        "description": "Keep Python packages isolated from your system Python.",
        "command": r"py -3.12 -m venv .venv && .venv\\Scripts\\activate",
    },
    {
        "step": 3,
        "title": "Install backend requirements",
        "description": "Install FastAPI, pytest, and rendering dependencies.",
        "command": "pip install -r requirements.txt",
    },
    {
        "step": 4,
        "title": "Create local environment file",
        "description": "Copy .env.example to .env. Keep .env out of Git.",
        "command": "copy .env.example .env",
    },
    {
        "step": 5,
        "title": "Bootstrap storage and database",
        "description": "Create folders, initialize SQLite tables, and optionally seed demo data.",
        "command": "python scripts/setup_project.py --seed-demo",
    },
    {
        "step": 6,
        "title": "Install frontend dependencies",
        "description": "Install the React/Vite frontend dependencies.",
        "command": "npm run frontend:install",
    },
    {
        "step": 7,
        "title": "Run backend and frontend",
        "description": "Start backend in one terminal and frontend in another terminal.",
        "command": "uvicorn app.main:app --reload  |  npm run frontend:dev",
    },
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _file_check(root: Path, relative: str) -> dict[str, str]:
    path = root / relative
    return {
        "label": relative,
        "status": "pass" if path.exists() else "fail",
        "detail": "Found" if path.exists() else "Missing setup file",
        "fix": "Restore this file before sharing the project." if not path.exists() else "",
    }


def build_setup_guide(project_root: str | Path = ".") -> dict[str, Any]:
    """Return a fresh-clone setup guide without changing local files."""
    root = Path(project_root).resolve()
    file_checks = [_file_check(root, item) for item in REQUIRED_SETUP_FILES]
    env_exists = (root / ".env").exists()
    db_exists = (root / "storage" / "app.db").exists()
    node_modules_exists = (root / "frontend" / "node_modules").exists()
    venv_exists = (root / ".venv").exists()

    quick_status = [
        {
            "label": ".env local config",
            "status": "pass" if env_exists else "warn",
            "detail": "Exists locally" if env_exists else "Not created yet; setup script can copy .env.example.",
        },
        {
            "label": "SQLite database",
            "status": "pass" if db_exists else "warn",
            "detail": "Exists locally" if db_exists else "Not created yet; run scripts/setup_project.py.",
        },
        {
            "label": "Python virtual environment",
            "status": "pass" if venv_exists else "manual",
            "detail": "Exists locally" if venv_exists else "Create with py -3.12 -m venv .venv.",
        },
        {
            "label": "Frontend node_modules",
            "status": "pass" if node_modules_exists else "manual",
            "detail": "Exists locally" if node_modules_exists else "Run npm run frontend:install.",
        },
    ]

    fail_count = sum(1 for item in file_checks if item["status"] == "fail")
    warn_count = sum(1 for item in quick_status if item["status"] == "warn")
    pass_count = sum(1 for item in file_checks + quick_status if item["status"] == "pass")

    markdown = build_setup_markdown(
        file_checks=file_checks,
        quick_status=quick_status,
        pass_count=pass_count,
        warn_count=warn_count,
        fail_count=fail_count,
    )

    return {
        "version": "0.28.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "fresh_clone_ready": fail_count == 0,
        },
        "setup_steps": SETUP_STEPS,
        "windows_setup_commands": WINDOWS_SETUP_COMMANDS,
        "backend_commands": BACKEND_COMMANDS,
        "frontend_commands": FRONTEND_COMMANDS,
        "git_commands": GIT_COMMANDS,
        "commit_message": COMMIT_MESSAGE,
        "required_setup_files": file_checks,
        "local_status": quick_status,
        "recommendations": [
            "Use setup_windows.bat for the fastest Windows setup.",
            "Use scripts/setup_project.py when you want a cross-platform Python bootstrap.",
            "Keep .env, .venv, frontend/node_modules, frontend/dist, storage/app.db, and generated media out of Git.",
            "After setup, run backend and frontend in separate terminals.",
            "Keep Ollama disabled on this laptop until you move AI generation to your other desktop.",
        ],
        "guide_markdown": markdown,
    }


def _status_table(title: str, rows: list[dict[str, str]]) -> str:
    lines = [f"## {title}", "", "| Status | Item | Detail | Fix |", "|---|---|---|---|"]
    for row in rows:
        lines.append(
            f"| {row.get('status', '')} | `{row.get('label', '')}` | {row.get('detail', '')} | {row.get('fix', '-') or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_setup_markdown(
    *,
    file_checks: list[dict[str, str]],
    quick_status: list[dict[str, str]],
    pass_count: int,
    warn_count: int,
    fail_count: int,
) -> str:
    lines = [
        "# Fresh Clone Setup Guide",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Summary: **{pass_count} passed**, **{warn_count} warnings**, **{fail_count} failures**.",
        "",
        "## Fast Windows Setup",
        "",
        "```bat",
        "setup_windows.bat",
        "```",
        "",
        "## Manual Windows Setup",
        "",
        "```bat",
        *WINDOWS_SETUP_COMMANDS,
        "```",
        "",
        "## Start Development Servers",
        "",
        "Backend terminal:",
        "",
        "```bat",
        *BACKEND_COMMANDS,
        "```",
        "",
        "Frontend terminal:",
        "",
        "```bat",
        *FRONTEND_COMMANDS,
        "```",
        "",
        "## Git Commands for This Step",
        "",
        "```bash",
        *GIT_COMMANDS,
        "```",
        "",
        _status_table("Required Setup Files", file_checks),
        _status_table("Local Machine Status", quick_status),
        "## Do Not Commit",
        "",
        "- `.env`",
        "- `.venv/`",
        "- `frontend/node_modules/`",
        "- `frontend/dist/`",
        "- `storage/app.db`",
        "- generated media/export folders under `storage/`",
        "- `__pycache__/` and `.pytest_cache/`",
        "",
    ]
    return "\n".join(lines)
