from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COMMIT_MESSAGE = "Add deployment packaging and production configuration guide"
VERSION = "0.33.0"

REQUIRED_FILES = [
    ".env.example",
    ".gitignore",
    "README.md",
    "NEXT_STEPS.md",
    "requirements.txt",
    "package.json",
    "frontend/package.json",
    "frontend/.env.example",
    "scripts/setup_project.py",
    "scripts/pre_push_check.py",
    "scripts/build_release_package.py",
    "docs/DEPLOYMENT_PRODUCTION_GUIDE.md",
]

PROTECTED_PATHS = [
    ".env",
    ".env.* except .env.example",
    ".venv/",
    "frontend/node_modules/",
    "frontend/dist/",
    "storage/app.db",
    "storage/exports/",
    "storage/audio/",
    "storage/video_drafts/",
    "storage/handoffs/",
    "storage/release_reports/",
    "storage/youtube_oauth/",
    "logs/",
    "dist_release/",
]

PRODUCTION_ENV_KEYS = [
    {
        "key": "ENVIRONMENT",
        "recommended": "production",
        "reason": "Makes logs, reports, and operator notes clearly distinguish production from local development.",
    },
    {
        "key": "AUTH_REQUIRED",
        "recommended": "true",
        "reason": "Production should not allow anonymous access to admin dashboards or publishing workflows.",
    },
    {
        "key": "DEFAULT_ADMIN_PASSWORD",
        "recommended": "change immediately",
        "reason": "Never deploy with the local demo password.",
    },
    {
        "key": "AUTH_COOKIE_SECURE",
        "recommended": "true when HTTPS is enabled",
        "reason": "Secure cookies should only travel over HTTPS in production.",
    },
    {
        "key": "CORS_ORIGINS",
        "recommended": "your real frontend domain only",
        "reason": "Avoid leaving broad localhost/dev origins as the only production configuration.",
    },
    {
        "key": "DATABASE_PATH",
        "recommended": "persistent disk path",
        "reason": "SQLite is acceptable for MVP demo hosting, but it must live on persistent storage.",
    },
    {
        "key": "YOUTUBE_API_ENABLED",
        "recommended": "false",
        "reason": "Manual upload remains the safe MVP publishing flow until API upload is fully implemented and tested.",
    },
]

PACKAGING_COMMANDS = [
    "python scripts/setup_project.py --check-only",
    "python -m pytest",
    "npm run frontend:install",
    "npm run frontend:build",
    "python scripts/pre_push_check.py",
    "python scripts/build_release_package.py",
]

GIT_COMMANDS = [
    "git status",
    "python scripts/setup_project.py --check-only",
    "python -m pytest",
    "npm run frontend:install",
    "npm run frontend:build",
    "python scripts/pre_push_check.py",
    "python scripts/build_release_package.py",
    "git status",
    "git add .",
    "git status",
    f"git commit -m \"{COMMIT_MESSAGE}\"",
    "git push",
]

DEPLOYMENT_STEPS = [
    {
        "phase": "1",
        "title": "Prepare production environment",
        "items": [
            "Copy .env.example to .env on the server, not in Git.",
            "Set AUTH_REQUIRED=true and change DEFAULT_ADMIN_PASSWORD before first public use.",
            "Set CORS_ORIGINS to the deployed frontend URL.",
            "Use persistent storage for database and generated package files.",
        ],
    },
    {
        "phase": "2",
        "title": "Build frontend",
        "items": [
            "Run npm run frontend:install once on the build machine.",
            "Run npm run frontend:build to create frontend/dist.",
            "Host frontend/dist on a static host or behind the same reverse proxy as FastAPI.",
        ],
    },
    {
        "phase": "3",
        "title": "Run backend",
        "items": [
            "Install Python requirements in a virtual environment.",
            "Run python scripts/setup_project.py --seed-demo only for demo deployments.",
            "Start FastAPI with uvicorn/gunicorn behind HTTPS reverse proxy for production-like hosting.",
        ],
    },
    {
        "phase": "4",
        "title": "Verify and rollback",
        "items": [
            "Check /api/health after deployment.",
            "Login with the production admin account and create one test package.",
            "Keep the previous release ZIP and database backup so you can rollback quickly.",
        ],
    },
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _status(found: bool) -> str:
    return "pass" if found else "warn"


def _build_required_file_checks(root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    for relative in REQUIRED_FILES:
        exists = (root / relative).exists()
        checks.append(
            {
                "status": "pass" if exists else "fail",
                "path": relative,
                "detail": "Found" if exists else "Missing required deployment file",
                "fix": "Create or restore this file before packaging." if not exists else "",
            }
        )
    return checks


def _build_gitignore_checks(root: Path) -> list[dict[str, str]]:
    gitignore_text = _read_text(root / ".gitignore")
    patterns = [
        ".env",
        "frontend/node_modules/",
        "frontend/dist/",
        "storage/app.db",
        "storage/exports/*",
        "storage/handoffs/*",
        "storage/release_reports/*",
        "storage/youtube_oauth/*",
        "*.log",
    ]
    return [
        {
            "status": _status(pattern in gitignore_text),
            "path": pattern,
            "detail": "Protected by .gitignore" if pattern in gitignore_text else "Pattern not found in .gitignore",
            "fix": f"Add `{pattern}` to .gitignore." if pattern not in gitignore_text else "",
        }
        for pattern in patterns
    ]


def _build_env_checks(root: Path) -> list[dict[str, str]]:
    env_example_text = _read_text(root / ".env.example")
    checks: list[dict[str, str]] = []
    for item in PRODUCTION_ENV_KEYS:
        found = any(line.strip().startswith(f"{item['key']}=") for line in env_example_text.splitlines())
        checks.append(
            {
                "status": _status(found),
                "key": item["key"],
                "recommended": item["recommended"],
                "reason": item["reason"],
                "detail": "Present in .env.example" if found else "Missing from .env.example",
                "fix": f"Add `{item['key']}=...` to .env.example." if not found else "",
            }
        )
    return checks


def _build_guide_markdown(
    *,
    required_file_checks: list[dict[str, str]],
    gitignore_checks: list[dict[str, str]],
    env_checks: list[dict[str, str]],
) -> str:
    lines = [
        "# Deployment Packaging and Production Configuration Guide",
        "",
        f"Version: `{VERSION}`",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This guide prepares the MVP for a safer shared ZIP, GitHub push, or simple production-like deployment.",
        "The app still supports local laptop development, but production should use stricter auth, real CORS origins, persistent storage, and a clean release package.",
        "",
        "## 1. Final local verification",
        "",
        "Run these commands before you push or share the ZIP:",
        "",
        "```bash",
        *PACKAGING_COMMANDS,
        "```",
        "",
        "## 2. Production `.env` checklist",
        "",
        "Copy `.env.example` to `.env` on the server. Do not commit `.env`.",
        "",
        "| Key | Recommended production value | Why |",
        "|---|---|---|",
    ]
    for item in env_checks:
        lines.append(f"| `{item['key']}` | {item['recommended']} | {item['reason']} |")

    lines.extend(
        [
            "",
            "Minimum production override example:",
            "",
            "```env",
            "ENVIRONMENT=production",
            "AUTH_REQUIRED=true",
            "DEFAULT_ADMIN_PASSWORD=replace-with-a-strong-password",
            "AUTH_COOKIE_SECURE=true",
            "CORS_ORIGINS=https://your-frontend-domain.example",
            "DATABASE_PATH=/persistent-storage/app.db",
            "YOUTUBE_API_ENABLED=false",
            "YOUTUBE_DRY_RUN=true",
            "```",
            "",
            "## 3. Release package command",
            "",
            "Use the new packaging helper to create a source ZIP without local databases, secrets, generated videos/audio, node_modules, or frontend build outputs:",
            "",
            "```bash",
            "python scripts/build_release_package.py",
            "```",
            "",
            "The default output is `dist_release/edu-content-platform-mvp-v33.zip`. The `dist_release/` folder is local output and should not be committed.",
            "",
            "## 4. Deployment options",
            "",
            "### Simple VPS / Windows server",
            "",
            "1. Install Python and Node.js.",
            "2. Extract the release ZIP.",
            "3. Create `.env` from `.env.example` and apply production overrides.",
            "4. Run `python -m venv .venv` and install `requirements.txt`.",
            "5. Run `python scripts/setup_project.py --seed-demo` only if you need demo data.",
            "6. Run FastAPI with `uvicorn app.main:app --host 0.0.0.0 --port 8000` behind HTTPS/reverse proxy.",
            "7. Build frontend with `npm run frontend:build` and serve `frontend/dist`.",
            "",
            "### Render / Railway style hosting",
            "",
            "- Backend build command: `pip install -r requirements.txt`.",
            "- Backend start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.",
            "- Frontend build command: `npm run frontend:install && npm run frontend:build`.",
            "- Frontend publish directory: `frontend/dist`.",
            "- Add all production `.env` values through the host's secret/environment UI.",
            "- Use a persistent disk/volume for SQLite database and generated package outputs.",
            "",
            "## 5. Backup and rollback",
            "",
            "- Back up `storage/app.db` before every production update.",
            "- Keep the last working release ZIP.",
            "- If a deployment breaks, stop the app, restore the previous ZIP and database backup, then restart.",
            "",
            "## 6. Required files check",
            "",
            "| Status | Path | Detail | Fix |",
            "|---|---|---|---|",
        ]
    )
    for item in required_file_checks:
        lines.append(f"| {item['status']} | `{item['path']}` | {item['detail']} | {item.get('fix') or '-'} |")

    lines.extend(
        [
            "",
            "## 7. Protected paths check",
            "",
            "| Status | Pattern | Detail | Fix |",
            "|---|---|---|---|",
        ]
    )
    for item in gitignore_checks:
        lines.append(f"| {item['status']} | `{item['path']}` | {item['detail']} | {item.get('fix') or '-'} |")

    lines.extend(
        [
            "",
            "## 8. Git commands",
            "",
            "```bash",
            *GIT_COMMANDS,
            "```",
            "",
            f"Commit message: `{COMMIT_MESSAGE}`",
            "",
        ]
    )
    return "\n".join(lines)


def build_deployment_config_guide(project_root: str | Path = ".") -> dict[str, Any]:
    """Build a deployment and production configuration guide without mutating the project."""
    root = Path(project_root).resolve()
    required_file_checks = _build_required_file_checks(root)
    gitignore_checks = _build_gitignore_checks(root)
    env_checks = _build_env_checks(root)

    all_checks = required_file_checks + gitignore_checks + env_checks
    fail_count = sum(1 for item in all_checks if item["status"] == "fail")
    warn_count = sum(1 for item in all_checks if item["status"] == "warn")
    pass_count = sum(1 for item in all_checks if item["status"] == "pass")

    guide_markdown = _build_guide_markdown(
        required_file_checks=required_file_checks,
        gitignore_checks=gitignore_checks,
        env_checks=env_checks,
    )

    recommendations = [
        "Keep .env, OAuth tokens, SQLite databases, generated media, node_modules, and release ZIP outputs out of Git.",
        "Use AUTH_REQUIRED=true and change DEFAULT_ADMIN_PASSWORD before any production or public demo deployment.",
        "Run the packaging script only after backend tests and frontend build pass.",
        "Keep manual YouTube publishing enabled until the future API adapter is fully tested in dry-run mode.",
    ]

    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "commit_message": COMMIT_MESSAGE,
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "ready_for_package": fail_count == 0,
        },
        "required_file_checks": required_file_checks,
        "gitignore_checks": gitignore_checks,
        "production_env_checks": env_checks,
        "protected_paths": PROTECTED_PATHS,
        "deployment_steps": DEPLOYMENT_STEPS,
        "packaging_commands": PACKAGING_COMMANDS,
        "git_commands": GIT_COMMANDS,
        "recommendations": recommendations,
        "guide_markdown": guide_markdown,
    }
