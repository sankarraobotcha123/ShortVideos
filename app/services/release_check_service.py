from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.config import settings

REQUIRED_GITIGNORE_PATTERNS = [
    ".env",
    ".venv/",
    "frontend/node_modules/",
    "frontend/dist/",
    "storage/app.db",
    "storage/exports/*",
    "storage/audio/*",
    "storage/video_drafts/*",
    "storage/asset_library/*",
    "storage/thumbnails/*",
    "storage/source_safety/*",
    "storage/trust_reviews/*",
    "storage/learning_outputs/*",
    "storage/release_reports/*",
    "__pycache__/",
    ".pytest_cache/",
]

REQUIRED_FILES = [
    "README.md",
    "NEXT_STEPS.md",
    ".gitignore",
    ".env.example",
    "requirements.txt",
    "package.json",
    "frontend/package.json",
    "scripts/init_db.py",
    "scripts/seed_demo_data.py",
    "scripts/setup_project.py",
    "setup_windows.bat",
    "setup_windows.ps1",
    "docs/FRESH_CLONE_SETUP.md",
    "app/routes/auth.py",
    "app/services/auth_service.py",
]

REQUIRED_DIRS = [
    "app",
    "app/routes",
    "app/services",
    "frontend/src",
    "tests",
    "storage",
    "storage/raw_uploads",
    "storage/scene_library",
]

REQUIRED_ENV_KEYS = [
    "APP_NAME",
    "DATABASE_PATH",
    "EXPORT_DIR",
    "AI_PROVIDER_CHAIN",
    "USE_OLLAMA",
    "USE_TRANSFORMERS",
    "TTS_PROVIDER_CHAIN",
    "USE_WINDOWS_SAPI_TTS",
    "USE_PYTTSX3_TTS",
    "FRONTEND_ASSET_VERSION",
    "AUTH_REQUIRED",
    "AUTH_TOKEN_TTL_HOURS",
    "DEFAULT_ADMIN_EMAIL",
    "DEFAULT_ADMIN_PASSWORD",
]

PROTECTED_PATHS = [
    ".env",
    ".venv/",
    "frontend/node_modules/",
    "frontend/dist/",
    "storage/app.db",
    "storage/exports/",
    "storage/audio/",
    "storage/video_drafts/",
    "storage/asset_library/",
    "storage/thumbnails/",
    "storage/source_safety/",
    "storage/trust_reviews/",
    "storage/learning_outputs/",
    "__pycache__/",
    ".pytest_cache/",
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
    "git commit -m \"Add content idea backlog and topic scoring workflow\"",
    "git push",
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _check(status: str, label: str, detail: str, fix: str = "") -> dict[str, str]:
    return {"status": status, "label": label, "detail": detail, "fix": fix}


def build_release_checklist(project_root: str | Path = ".") -> dict[str, Any]:
    """Build a GitHub/release readiness checklist without mutating the project."""
    root = Path(project_root).resolve()
    gitignore_text = _read_text(root / ".gitignore")
    env_example_text = _read_text(root / ".env.example")

    file_checks = []
    for relative in REQUIRED_FILES:
        exists = (root / relative).exists()
        file_checks.append(
            _check(
                "pass" if exists else "fail",
                relative,
                "Found" if exists else "Missing required project file",
                "Create or restore this file before release." if not exists else "",
            )
        )

    dir_checks = []
    for relative in REQUIRED_DIRS:
        path = root / relative
        exists = path.exists() and path.is_dir()
        has_gitkeep = (path / ".gitkeep").exists()
        status = "pass" if exists else "fail"
        if exists and relative.startswith("storage") and relative != "storage" and not has_gitkeep:
            status = "warn"
        dir_checks.append(
            _check(
                status,
                relative,
                "Found" + (" with .gitkeep" if has_gitkeep else "") if exists else "Missing required folder",
                "Add the folder and a .gitkeep file if it must be tracked." if status != "pass" else "",
            )
        )

    gitignore_checks = []
    for pattern in REQUIRED_GITIGNORE_PATTERNS:
        found = pattern in gitignore_text
        gitignore_checks.append(
            _check(
                "pass" if found else "fail",
                pattern,
                "Ignored" if found else "Pattern missing from .gitignore",
                f"Add `{pattern}` to .gitignore." if not found else "",
            )
        )

    env_checks = []
    for key in REQUIRED_ENV_KEYS:
        found = any(line.strip().startswith(f"{key}=") for line in env_example_text.splitlines())
        env_checks.append(
            _check(
                "pass" if found else "warn",
                key,
                "Present in .env.example" if found else "Missing from .env.example",
                f"Add `{key}=...` to .env.example." if not found else "",
            )
        )

    command_checks = [
        _check("manual", "Backend tests", "Run `python -m pytest` before each push.", "Fix failing tests before committing."),
        _check("manual", "Frontend build", "Run `npm run frontend:build` before release.", "Fix Vite/React build errors before committing."),
        _check("manual", "Git status", "Run `git status` before and after `git add .`.", "Remove generated files from staging if they appear."),
    ]

    all_checks = file_checks + dir_checks + gitignore_checks + env_checks
    fail_count = sum(1 for item in all_checks if item["status"] == "fail")
    warn_count = sum(1 for item in all_checks if item["status"] == "warn")
    pass_count = sum(1 for item in all_checks if item["status"] == "pass")

    recommendations = []
    if fail_count:
        recommendations.append("Fix failed release checks before pushing to GitHub.")
    if warn_count:
        recommendations.append("Review warnings. Some may be acceptable, but confirm before release.")
    recommendations.append("Do not commit generated media, local databases, virtual environments, node_modules, or .env files.")
    recommendations.append("Run backend tests and frontend build before pushing a release commit.")
    recommendations.append("Use the exact commit message for this step: Add content idea backlog and topic scoring workflow")

    report_markdown = build_release_report_markdown(
        pass_count=pass_count,
        warn_count=warn_count,
        fail_count=fail_count,
        file_checks=file_checks,
        dir_checks=dir_checks,
        gitignore_checks=gitignore_checks,
        env_checks=env_checks,
        command_checks=command_checks,
        recommendations=recommendations,
    )

    return {
        "version": "0.25.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "ready_for_push": fail_count == 0,
        },
        "file_checks": file_checks,
        "directory_checks": dir_checks,
        "gitignore_checks": gitignore_checks,
        "env_example_checks": env_checks,
        "manual_command_checks": command_checks,
        "protected_paths": PROTECTED_PATHS,
        "git_commands": GIT_COMMANDS,
        "commit_message": "Add content production board workflow",
        "recommendations": recommendations,
        "report_markdown": report_markdown,
        "settings_snapshot": {
            "database_path": str(settings.database_path),
            "export_dir": str(settings.export_dir),
            "ai_provider_chain": settings.ai_provider_chain,
            "tts_provider_chain": settings.tts_provider_chain,
            "frontend_asset_version": settings.frontend_asset_version,
        },
    }


def _check_table(title: str, checks: list[dict[str, str]]) -> str:
    lines = [f"## {title}", "", "| Status | Item | Detail | Fix |", "|---|---|---|---|"]
    for item in checks:
        lines.append(
            f"| {item['status']} | `{item['label']}` | {item['detail']} | {item.get('fix') or '-'} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_release_report_markdown(
    *,
    pass_count: int,
    warn_count: int,
    fail_count: int,
    file_checks: list[dict[str, str]],
    dir_checks: list[dict[str, str]],
    gitignore_checks: list[dict[str, str]],
    env_checks: list[dict[str, str]],
    command_checks: list[dict[str, str]],
    recommendations: list[str],
) -> str:
    lines = [
        "# Production Cleanup and Release Checklist",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Summary: **{pass_count} passed**, **{warn_count} warnings**, **{fail_count} failures**.",
        "",
        "## Recommended Git Commands",
        "",
        "```bash",
        *GIT_COMMANDS,
        "```",
        "",
        "## Do Not Commit These Paths",
        "",
    ]
    lines.extend([f"- `{path}`" for path in PROTECTED_PATHS])
    lines.append("")
    lines.append(_check_table("Required Files", file_checks))
    lines.append(_check_table("Required Folders", dir_checks))
    lines.append(_check_table(".gitignore Checks", gitignore_checks))
    lines.append(_check_table(".env.example Checks", env_checks))
    lines.append(_check_table("Manual Verification Commands", command_checks))
    lines.append("## Recommendations")
    lines.append("")
    lines.extend([f"- {item}" for item in recommendations])
    lines.append("")
    return "\n".join(lines)
