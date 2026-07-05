from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COMMIT_MESSAGE = "Add final project audit and test stability tools"
VERSION = "0.34.0"

GIT_COMMANDS = [
    "git status",
    "python scripts/setup_project.py --check-only",
    "python scripts/run_tests.py",
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

MANUAL_QA_STEPS = [
    {
        "area": "Login and protected downloads",
        "steps": [
            "Open the React app on http://127.0.0.1:5173.",
            "Login as the local admin after setting AUTH_REQUIRED=true in .env.",
            "Open Release checklist, Deployment guide, YouTube publishing, and Final MVP polish pages.",
            "Click each download button and confirm the markdown file opens or downloads while logged in.",
        ],
    },
    {
        "area": "Core content workflow",
        "steps": [
            "Create one package from the Create package page.",
            "Open the package detail page and run source safety, trust review, learning output, thumbnail guide, assembly plan, and video draft checks as needed.",
            "Approve the publishing gate only after the checklist passes.",
        ],
    },
    {
        "area": "Planning and publishing workflow",
        "steps": [
            "Create or open a batch and assign a package.",
            "Bulk schedule the batch to the calendar.",
            "Open the production board and move one card through the visible stages.",
            "Use YouTube publishing checklist before manually uploading to YouTube Studio.",
        ],
    },
    {
        "area": "Responsive UI check",
        "steps": [
            "Resize the browser to mobile width or use DevTools mobile preview.",
            "Confirm the sidebar becomes readable, active page remains highlighted, and tables/cards do not overflow badly.",
            "Use keyboard Tab navigation to confirm visible focus on links, buttons, inputs, and selects.",
        ],
    },
]

POLISH_WORK_ITEMS = [
    {
        "key": "cross_origin_auth_cookies",
        "title": "Cross-port auth cookie support",
        "status": "pass",
        "detail": "Frontend requests now use credentials=include so browser cookies work when React and FastAPI run on different ports.",
    },
    {
        "key": "active_sidebar_state",
        "title": "Clear active sidebar state",
        "status": "pass",
        "detail": "Sidebar keeps the current page chip and active link styling so the user can see the current section clearly.",
    },
    {
        "key": "keyboard_focus",
        "title": "Keyboard focus visibility",
        "status": "pass",
        "detail": "Final CSS adds visible focus rings for links, buttons, inputs, selects, textareas, and package rows.",
    },
    {
        "key": "mobile_layout",
        "title": "Mobile and narrow-screen layout",
        "status": "pass",
        "detail": "Final CSS tightens responsive sidebar, cards, quick actions, tables, and form controls for smaller screens.",
    },
    {
        "key": "release_packaging",
        "title": "Clean release packaging",
        "status": "pass",
        "detail": "Release builder now targets v34 and continues excluding databases, node_modules, OAuth secrets, generated media, caches, and logs.",
    },
    {
        "key": "stable_test_runner",
        "title": "Stable backend test runner",
        "status": "pass",
        "detail": "Added scripts/run_tests.py to run pytest with third-party plugin autoload disabled for stable laptop and CI test runs.",
    },
    {
        "key": "local_artifact_cleanup",
        "title": "Safe local artifact cleanup",
        "status": "pass",
        "detail": "Added scripts/clean_local_artifacts.py to preview or remove cache/build outputs before Git pushes without deleting project data.",
    },
    {
        "key": "manual_qa",
        "title": "Manual MVP QA checklist",
        "status": "manual",
        "detail": "Use the manual steps in this report for a last browser check before pushing or submitting the MVP.",
    },
]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _count(conn, sql: str) -> int:
    if conn is None:
        return 0
    try:
        row = conn.execute(sql).fetchone()
        if row is None:
            return 0
        return int(row[0] or 0)
    except Exception:
        return 0


def _project_check(status: str, label: str, detail: str, fix: str = "") -> dict[str, str]:
    return {"status": status, "label": label, "detail": detail, "fix": fix}


def _build_project_checks(root: Path) -> list[dict[str, str]]:
    app_text = _read_text(root / "frontend/src/App.jsx")
    api_text = _read_text(root / "frontend/src/api.js")
    styles_text = _read_text(root / "frontend/src/styles.css")
    gitignore_text = _read_text(root / ".gitignore")

    checks = [
        _project_check(
            "pass" if "credentials: 'include'" in api_text or 'credentials: "include"' in api_text else "fail",
            "frontend/src/api.js auth credentials",
            "Cross-port cookie credentials enabled" if "credentials: 'include'" in api_text or 'credentials: "include"' in api_text else "Frontend requests may not persist API auth cookies across ports",
            "Set fetch credentials to include in the shared request helper.",
        ),
        _project_check(
            "pass" if "current-page-chip" in app_text and "nav a.active" in styles_text else "warn",
            "Sidebar current-page indicator",
            "Current page chip and active nav styling found" if "current-page-chip" in app_text and "nav a.active" in styles_text else "Active page styling should be checked manually",
            "Keep the current-page chip and nav active class visible.",
        ),
        _project_check(
            "pass" if ":focus-visible" in styles_text else "warn",
            "Keyboard focus states",
            "Visible focus CSS found" if ":focus-visible" in styles_text else "Keyboard focus CSS not found",
            "Add focus-visible styling for keyboard navigation.",
        ),
        _project_check(
            "pass" if "@media (max-width: 640px)" in styles_text and "@media (max-width: 980px)" in styles_text else "warn",
            "Responsive layout polish",
            "Mobile and tablet responsive rules found" if "@media (max-width: 640px)" in styles_text and "@media (max-width: 980px)" in styles_text else "Responsive CSS should be checked manually",
            "Add narrow-screen rules for sidebar, cards, buttons, and forms.",
        ),
        _project_check(
            "pass" if (root / "docs/FINAL_MVP_POLISH.md").exists() else "fail",
            "docs/FINAL_MVP_POLISH.md",
            "Final polish documentation found" if (root / "docs/FINAL_MVP_POLISH.md").exists() else "Final polish documentation missing",
            "Create docs/FINAL_MVP_POLISH.md.",
        ),
        _project_check(
            "pass" if (root / "scripts/run_tests.py").exists() else "fail",
            "scripts/run_tests.py",
            "Stable test runner found" if (root / "scripts/run_tests.py").exists() else "Stable test runner missing",
            "Create scripts/run_tests.py for stable backend test execution.",
        ),
        _project_check(
            "pass" if (root / "scripts/clean_local_artifacts.py").exists() else "fail",
            "scripts/clean_local_artifacts.py",
            "Local cleanup helper found" if (root / "scripts/clean_local_artifacts.py").exists() else "Local cleanup helper missing",
            "Create scripts/clean_local_artifacts.py for cache/build cleanup before Git pushes.",
        ),
        _project_check(
            "pass" if (root / "docs/PROJECT_AUDIT_V34.md").exists() else "fail",
            "docs/PROJECT_AUDIT_V34.md",
            "Project audit documentation found" if (root / "docs/PROJECT_AUDIT_V34.md").exists() else "Project audit documentation missing",
            "Create docs/PROJECT_AUDIT_V34.md.",
        ),
        _project_check(
            "pass" if "storage/youtube_oauth/*" in gitignore_text and "dist_release/" in gitignore_text else "warn",
            "Generated/secret file protection",
            "Important generated and OAuth paths are ignored" if "storage/youtube_oauth/*" in gitignore_text and "dist_release/" in gitignore_text else "Review .gitignore before pushing",
            "Keep generated assets, OAuth files, .env, node_modules, and release zips out of Git.",
        ),
    ]
    return checks


def _build_db_snapshot(conn) -> dict[str, int]:
    return {
        "packages": _count(conn, "SELECT COUNT(*) FROM content_packages"),
        "approved_packages": _count(conn, "SELECT COUNT(*) FROM content_packages WHERE review_status = 'approved'"),
        "published_packages": _count(conn, "SELECT COUNT(*) FROM content_packages WHERE review_status = 'published'"),
        "batches": _count(conn, "SELECT COUNT(*) FROM content_batches"),
        "calendar_items": _count(conn, "SELECT COUNT(*) FROM publishing_calendar"),
        "visual_assets": _count(conn, "SELECT COUNT(*) FROM visual_assets"),
        "ideas": _count(conn, "SELECT COUNT(*) FROM content_ideas"),
        "series": _count(conn, "SELECT COUNT(*) FROM content_series"),
        "multilingual_plans": _count(conn, "SELECT COUNT(*) FROM multilingual_plans"),
        "prompt_templates": _count(conn, "SELECT COUNT(*) FROM prompt_templates"),
    }


def _build_report_markdown(
    *,
    project_checks: list[dict[str, str]],
    db_snapshot: dict[str, int],
    recommendations: list[str],
) -> str:
    lines = [
        "# Final MVP Bug-fix and UI Polish Report",
        "",
        f"Version: `{VERSION}`",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This is the final MVP pass after the provider setup guide, YouTube publishing checklist, and deployment packaging guide.",
        "The goal is not to add a large new feature. The goal is to make the MVP safer to run, easier to navigate, and clearer before pushing to GitHub or sharing the ZIP.",
        "",
        "## Completed fixes and polish",
        "",
    ]
    for item in POLISH_WORK_ITEMS:
        lines.append(f"- **{item['title']}** — {item['detail']}")

    lines.extend([
        "",
        "## Project checks",
        "",
        "| Status | Item | Detail | Fix |",
        "|---|---|---|---|",
    ])
    for item in project_checks:
        lines.append(f"| {item['status']} | {item['label']} | {item['detail']} | {item.get('fix') or '-'} |")

    lines.extend([
        "",
        "## Current data snapshot",
        "",
        "| Area | Count |",
        "|---|---:|",
    ])
    for key, value in db_snapshot.items():
        lines.append(f"| {key.replace('_', ' ').title()} | {value} |")

    lines.extend([
        "",
        "## Manual QA before final push",
        "",
    ])
    for group in MANUAL_QA_STEPS:
        lines.append(f"### {group['area']}")
        for step in group["steps"]:
            lines.append(f"- {step}")
        lines.append("")

    lines.extend([
        "## Recommended Git commands",
        "",
        "```bash",
        *GIT_COMMANDS,
        "```",
        "",
        "## Recommendations",
        "",
    ])
    for item in recommendations:
        lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def build_final_polish_report(conn=None, project_root: str | Path = ".") -> dict[str, Any]:
    """Return the final MVP polish report without mutating project data."""
    root = Path(project_root).resolve()
    project_checks = _build_project_checks(root)
    db_snapshot = _build_db_snapshot(conn)

    fail_count = sum(1 for item in project_checks if item["status"] == "fail")
    warn_count = sum(1 for item in project_checks if item["status"] == "warn")
    pass_count = sum(1 for item in project_checks if item["status"] == "pass")

    recommendations = [
        "Run backend tests through `scripts/run_tests.py` and the frontend build on your machine before pushing.",
        "Keep AUTH_REQUIRED=false only for solo local development; set AUTH_REQUIRED=true for demos or shared usage.",
        "Use the YouTube publishing checklist for manual upload until the API upload adapter is fully implemented and tested.",
        "Do one browser QA pass at desktop and mobile width before submitting the final MVP.",
        f"Use the exact commit message for this step: {COMMIT_MESSAGE}",
    ]

    report_markdown = _build_report_markdown(
        project_checks=project_checks,
        db_snapshot=db_snapshot,
        recommendations=recommendations,
    )

    return {
        "version": VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "commit_message": COMMIT_MESSAGE,
            "pass_count": pass_count,
            "warn_count": warn_count,
            "fail_count": fail_count,
            "mvp_final_ready": fail_count == 0,
        },
        "completed_items": POLISH_WORK_ITEMS,
        "project_checks": project_checks,
        "db_snapshot": db_snapshot,
        "manual_qa_steps": MANUAL_QA_STEPS,
        "git_commands": GIT_COMMANDS,
        "commit_message": COMMIT_MESSAGE,
        "recommendations": recommendations,
        "report_markdown": report_markdown,
    }
