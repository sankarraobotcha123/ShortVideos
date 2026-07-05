from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.config import settings

COMMIT_MESSAGE = "Add YouTube publishing checklist workflow"

YOUTUBE_SAFE_ENV = """YOUTUBE_API_ENABLED=false
YOUTUBE_DRY_RUN=true
YOUTUBE_OAUTH_DIR=storage/youtube_oauth
YOUTUBE_CLIENT_SECRETS_FILE=storage/youtube_oauth/client_secret.json
YOUTUBE_TOKEN_FILE=storage/youtube_oauth/token.json
YOUTUBE_CHANNEL_ID=
YOUTUBE_DEFAULT_PRIVACY_STATUS=private
YOUTUBE_DEFAULT_PLAYLIST_ID=
YOUTUBE_NOTIFY_SUBSCRIBERS=false
""".strip()

YOUTUBE_API_PREP_ENV = """YOUTUBE_API_ENABLED=true
YOUTUBE_DRY_RUN=true
YOUTUBE_OAUTH_DIR=storage/youtube_oauth
YOUTUBE_CLIENT_SECRETS_FILE=storage/youtube_oauth/client_secret.json
YOUTUBE_TOKEN_FILE=storage/youtube_oauth/token.json
YOUTUBE_CHANNEL_ID=replace_after_channel_verification
YOUTUBE_DEFAULT_PRIVACY_STATUS=private
YOUTUBE_DEFAULT_PLAYLIST_ID=optional_playlist_id
YOUTUBE_NOTIFY_SUBSCRIBERS=false
""".strip()

MANUAL_PUBLISHING_PHASES = [
    {
        "key": "final_review",
        "title": "Final package review",
        "goal": "Confirm the Short is safe, useful, and ready before opening YouTube Studio.",
        "items": [
            "Review script, subtitles, title options, description, hashtags, and quiz question.",
            "Confirm source safety review and teacher trust review are complete.",
            "Confirm publishing approval gate is approved before marking anything as published.",
            "Check final video duration, spelling, audio clarity, and visual readability on mobile size.",
        ],
    },
    {
        "key": "assets_ready",
        "title": "Export and asset readiness",
        "goal": "Prepare upload files and copy blocks without searching inside the project again.",
        "items": [
            "Export the package ZIP and keep README, subtitle file, script, visual prompts, and video draft together.",
            "Open the MP4/video draft or editor-exported final video and watch it fully once.",
            "Prepare the thumbnail manually in Canva/CapCut if a thumbnail guide exists.",
            "Copy one final title, description, and hashtag set into a publishing note.",
        ],
    },
    {
        "key": "youtube_studio_upload",
        "title": "YouTube Studio manual upload",
        "goal": "Publish safely without API risk while the MVP is still being validated.",
        "items": [
            "Upload the final MP4 in YouTube Studio, not through API automation yet.",
            "Paste the selected title, description, hashtags, playlist, and language metadata.",
            "Choose the correct audience and visibility settings manually after reviewing the video.",
            "Keep visibility private/unlisted first if you want one final mobile preview before public release.",
        ],
    },
    {
        "key": "after_publish",
        "title": "After publishing",
        "goal": "Keep the app database aligned with the real channel state.",
        "items": [
            "Copy the YouTube video URL into the package/calendar notes.",
            "Update the calendar actual publish date and status.",
            "Mark the package as published only after the real upload is live.",
            "Enter manual analytics after enough views are collected so future topics can improve.",
        ],
    },
]

API_PREP_STEPS = [
    {
        "step": 1,
        "title": "Keep API mode disabled during MVP validation",
        "description": "Manual publishing is safer until title style, video format, upload cadence, and review gates are stable.",
        "owner_action": "Use YOUTUBE_API_ENABLED=false and YOUTUBE_DRY_RUN=true.",
    },
    {
        "step": 2,
        "title": "Prepare OAuth files outside Git",
        "description": "Client secrets and token files belong only in local storage/youtube_oauth and must stay ignored by Git.",
        "owner_action": "Create the files locally later; never place real secrets in docs, commits, or screenshots.",
    },
    {
        "step": 3,
        "title": "Add an upload adapter behind a one-method interface",
        "description": "Future code should receive a validated package and return dry-run/upload results without changing business logic.",
        "owner_action": "Implement only after manual publishing proves the workflow.",
    },
    {
        "step": 4,
        "title": "Dry-run before any real upload",
        "description": "The first API version should validate title, description, tags, file path, privacy status, and playlist without uploading.",
        "owner_action": "Keep YOUTUBE_DRY_RUN=true until you intentionally test on a private video.",
    },
]

API_SAFETY_BOUNDARIES = [
    "No automatic upload is implemented in this step.",
    "No YouTube OAuth secrets, refresh tokens, or API keys are committed.",
    "Manual review and publishing approval remain required before upload.",
    "Future API mode should default to private visibility and dry-run validation.",
    "Analytics sync is still manual until the MVP content format proves useful.",
]

TEST_COMMANDS = [
    "python scripts/setup_project.py --check-only",
    "python scripts/run_tests.py",
    "npm run frontend:build",
    "uvicorn app.main:app --reload",
    "Open http://127.0.0.1:5173/#/youtube-publishing",
    "Download the checklist and use it for one manually uploaded Short",
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

REQUIRED_ENV_KEYS = [
    "YOUTUBE_API_ENABLED",
    "YOUTUBE_DRY_RUN",
    "YOUTUBE_OAUTH_DIR",
    "YOUTUBE_CLIENT_SECRETS_FILE",
    "YOUTUBE_TOKEN_FILE",
    "YOUTUBE_CHANNEL_ID",
    "YOUTUBE_DEFAULT_PRIVACY_STATUS",
    "YOUTUBE_DEFAULT_PLAYLIST_ID",
    "YOUTUBE_NOTIFY_SUBSCRIBERS",
]


def _read_env_example(project_root: Path) -> str:
    try:
        return (project_root / ".env.example").read_text(encoding="utf-8")
    except Exception:
        return ""


def _env_key_status(project_root: Path) -> list[dict[str, str]]:
    env_text = _read_env_example(project_root)
    checks: list[dict[str, str]] = []
    for key in REQUIRED_ENV_KEYS:
        found = any(line.strip().startswith(f"{key}=") for line in env_text.splitlines())
        checks.append(
            {
                "key": key,
                "status": "pass" if found else "warn",
                "detail": "Present in .env.example" if found else "Missing from .env.example",
            }
        )
    return checks


def _json_list(value: str | None) -> list[Any]:
    try:
        parsed = json.loads(value or "[]")
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def _best_title(title_options: str | None, topic: str) -> str:
    options = [str(item).strip() for item in _json_list(title_options) if str(item).strip()]
    return options[0] if options else topic


def _row_readiness(row: dict[str, Any]) -> dict[str, Any]:
    review_status = row.get("review_status") or "draft"
    gate_status = row.get("gate_status") or "not_created"
    calendar_status = row.get("calendar_status") or "unscheduled"
    trust_score = int(row.get("trust_score") or 0)
    missing: list[str] = []

    if review_status not in {"approved", "published"}:
        missing.append("approve package review")
    if gate_status != "approved" and review_status != "published":
        missing.append("approve publishing gate")
    if trust_score < 70:
        missing.append("raise teacher trust score")
    if not row.get("description"):
        missing.append("final description")
    if not _json_list(row.get("hashtags")):
        missing.append("hashtags")

    if review_status == "published" or calendar_status == "published":
        readiness = "published"
        next_action = "Collect analytics and update manual analytics."
    elif not missing:
        readiness = "ready_to_upload"
        next_action = "Open YouTube Studio and use the manual publishing checklist."
    elif "approve publishing gate" in missing:
        readiness = "needs_gate"
        next_action = "Create or approve the publishing approval gate before upload."
    elif "approve package review" in missing:
        readiness = "needs_review"
        next_action = "Finish script/content review, then run safety/trust/publishing checks."
    else:
        readiness = "needs_polish"
        next_action = "Complete the missing publishing copy or quality checks."

    return {
        "readiness": readiness,
        "next_action": next_action,
        "missing_items": missing,
    }


def build_package_readiness(conn: Any | None = None, limit: int = 50) -> list[dict[str, Any]]:
    if conn is None:
        return []

    rows = conn.execute(
        """
        SELECT
          cp.id, cp.topic, cp.subject, cp.class_level, cp.language, cp.review_status,
          cp.trust_score, cp.title_options, cp.description, cp.hashtags, cp.created_at,
          pc.planned_publish_date, pc.actual_publish_date, pc.status AS calendar_status,
          pc.platform, pc.playlist_name,
          pa.gate_status, pa.status AS approval_status, pa.reviewer_decision AS approval_decision
        FROM content_packages cp
        LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
        LEFT JOIN publishing_approvals pa ON pa.id = (
            SELECT id FROM publishing_approvals
            WHERE package_id = cp.id
            ORDER BY id DESC
            LIMIT 1
        )
        ORDER BY
          CASE WHEN pc.planned_publish_date IS NULL OR pc.planned_publish_date = '' THEN 1 ELSE 0 END,
          pc.planned_publish_date ASC,
          cp.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    packages = []
    for raw in rows:
        row = dict(raw)
        readiness = _row_readiness(row)
        packages.append(
            {
                "id": int(row["id"]),
                "topic": row.get("topic") or "",
                "subject": row.get("subject") or "",
                "class_level": row.get("class_level") or "",
                "language": row.get("language") or "English",
                "best_title": _best_title(row.get("title_options"), row.get("topic") or "Untitled Short"),
                "review_status": row.get("review_status") or "draft",
                "trust_score": int(row.get("trust_score") or 0),
                "gate_status": row.get("gate_status") or "not_created",
                "approval_status": row.get("approval_status") or "not_created",
                "calendar_status": row.get("calendar_status") or "unscheduled",
                "planned_publish_date": row.get("planned_publish_date") or "",
                "actual_publish_date": row.get("actual_publish_date") or "",
                "platform": row.get("platform") or "YouTube Shorts",
                "playlist_name": row.get("playlist_name") or "",
                **readiness,
            }
        )
    return packages


def _summary(packages: list[dict[str, Any]], env_checks: list[dict[str, str]]) -> dict[str, Any]:
    ready_count = sum(1 for item in packages if item["readiness"] == "ready_to_upload")
    needs_gate_count = sum(1 for item in packages if item["readiness"] == "needs_gate")
    scheduled_count = sum(1 for item in packages if item["calendar_status"] in {"planned", "scheduled"})
    published_count = sum(1 for item in packages if item["readiness"] == "published")
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "manual_upload_first": True,
        "api_enabled": settings.youtube_api_enabled,
        "dry_run": settings.youtube_dry_run,
        "total_packages_checked": len(packages),
        "ready_to_upload_count": ready_count,
        "needs_gate_count": needs_gate_count,
        "scheduled_count": scheduled_count,
        "published_count": published_count,
        "env_checks_passed": sum(1 for item in env_checks if item["status"] == "pass"),
        "env_checks_warnings": sum(1 for item in env_checks if item["status"] != "pass"),
        "commit_message": COMMIT_MESSAGE,
    }


def build_youtube_publishing_checklist(
    conn: Any | None = None,
    project_root: str | Path = ".",
    limit: int = 50,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    packages = build_package_readiness(conn, limit=limit)
    env_checks = _env_key_status(root)
    env_profiles = [
        {
            "key": "manual_safe",
            "title": "Manual publishing safe mode",
            "recommended_for": "Current MVP publishing from YouTube Studio.",
            "env": YOUTUBE_SAFE_ENV,
            "when_to_use": "Use this now. It avoids OAuth/API upload risk and keeps the workflow manual.",
        },
        {
            "key": "api_dry_run_prep",
            "title": "Optional API dry-run preparation",
            "recommended_for": "Future upload adapter experiments after manual publishing is stable.",
            "env": YOUTUBE_API_PREP_ENV,
            "when_to_use": "Use later only for dry-run validation first. Do not upload automatically in this MVP step.",
        },
    ]
    summary = _summary(packages, env_checks)
    markdown = build_youtube_publishing_markdown(
        summary=summary,
        packages=packages,
        env_profiles=env_profiles,
        env_checks=env_checks,
    )
    return {
        "summary": summary,
        "manual_publishing_phases": MANUAL_PUBLISHING_PHASES,
        "api_prep_steps": API_PREP_STEPS,
        "api_safety_boundaries": API_SAFETY_BOUNDARIES,
        "env_profiles": env_profiles,
        "env_checks": env_checks,
        "package_readiness": packages,
        "test_commands": TEST_COMMANDS,
        "git_commands": GIT_COMMANDS,
        "guide_markdown": markdown,
        "settings_snapshot": {
            "youtube_api_enabled": settings.youtube_api_enabled,
            "youtube_dry_run": settings.youtube_dry_run,
            "youtube_oauth_dir": str(settings.youtube_oauth_dir),
            "youtube_default_privacy_status": settings.youtube_default_privacy_status,
            "youtube_channel_id_configured": bool(settings.youtube_channel_id),
        },
    }


def build_youtube_publishing_markdown(
    *,
    summary: dict[str, Any],
    packages: list[dict[str, Any]],
    env_profiles: list[dict[str, str]],
    env_checks: list[dict[str, str]],
) -> str:
    lines = [
        "# YouTube Manual Publishing Checklist",
        "",
        "This workflow keeps publishing manual for the MVP while preparing safe placeholders for a future YouTube API adapter.",
        "No automatic YouTube upload is implemented in this step.",
        "",
        "## Summary",
        "",
        f"- Packages checked: {summary['total_packages_checked']}",
        f"- Ready to upload: {summary['ready_to_upload_count']}",
        f"- Needs publishing gate: {summary['needs_gate_count']}",
        f"- Scheduled: {summary['scheduled_count']}",
        f"- Published: {summary['published_count']}",
        f"- API enabled: {summary['api_enabled']}",
        f"- API dry-run: {summary['dry_run']}",
        "",
        "## Manual publishing phases",
        "",
    ]
    for phase in MANUAL_PUBLISHING_PHASES:
        lines.extend([f"### {phase['title']}", "", phase["goal"], ""])
        lines.extend([f"- {item}" for item in phase["items"]])
        lines.append("")

    lines.extend([
        "## Package readiness",
        "",
        "| ID | Title | Review | Gate | Calendar | Readiness | Next action |",
        "|---:|---|---|---|---|---|---|",
    ])
    if packages:
        for item in packages:
            lines.append(
                f"| {item['id']} | {item['best_title']} | {item['review_status']} | {item['gate_status']} | {item['calendar_status']} | {item['readiness']} | {item['next_action']} |"
            )
    else:
        lines.append("| - | No packages yet | - | - | - | - | Create and approve one package first. |")

    lines.extend([
        "",
        "## Optional YouTube API preparation",
        "",
    ])
    for step in API_PREP_STEPS:
        lines.extend([
            f"### {step['step']}. {step['title']}",
            "",
            step["description"],
            "",
            f"Action: {step['owner_action']}",
            "",
        ])

    lines.extend([
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
        "## .env.example YouTube keys",
        "",
        "| Key | Status | Detail |",
        "|---|---|---|",
    ])
    for item in env_checks:
        lines.append(f"| {item['key']} | {item['status']} | {item['detail']} |")

    lines.extend([
        "",
        "## API safety boundaries",
        "",
    ])
    lines.extend([f"- {item}" for item in API_SAFETY_BOUNDARIES])
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
    ])
    return "\n".join(lines)
