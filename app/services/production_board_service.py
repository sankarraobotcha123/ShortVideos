from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from datetime import date
from typing import Any

PRODUCTION_STAGES: list[dict[str, str]] = [
    {
        "key": "script_review",
        "label": "Script Review",
        "description": "Generated package exists, but the script still needs human review/editing.",
        "exit_criteria": "Script is checked, edited if needed, and review_status becomes approved.",
    },
    {
        "key": "script_revision",
        "label": "Script Revision",
        "description": "Script needs changes before moving into production assets.",
        "exit_criteria": "Reviewer changes status from edit_required/rejected to approved.",
    },
    {
        "key": "production_assets",
        "label": "Production Assets",
        "description": "Prepare narration, thumbnail guide, reusable visuals, assembly plan, and video draft.",
        "exit_criteria": "At least the required production helpers are generated for editing/publishing.",
    },
    {
        "key": "source_safety",
        "label": "Source Safety",
        "description": "Run originality/source review to avoid copied textbook-style content.",
        "exit_criteria": "Latest source safety risk is low/medium and not blocked by copied text issues.",
    },
    {
        "key": "teacher_review",
        "label": "Teacher Trust Review",
        "description": "Run quality review for factual accuracy, age fit, clarity, and confidence.",
        "exit_criteria": "Teacher Trust Score is acceptable and reviewer decision is approved or ready.",
    },
    {
        "key": "publishing_gate",
        "label": "Publishing Gate",
        "description": "Final gate before export/publishing: checks review, safety, trust score, package readiness.",
        "exit_criteria": "Publishing gate is approved by a publisher/reviewer.",
    },
    {
        "key": "ready_to_publish",
        "label": "Ready to Publish",
        "description": "Final export is allowed. Upload/schedule the Short manually.",
        "exit_criteria": "Calendar entry is planned/scheduled or actual publish date is recorded.",
    },
    {
        "key": "scheduled",
        "label": "Scheduled",
        "description": "Short is scheduled on the publishing calendar.",
        "exit_criteria": "Short is published and analytics collection starts.",
    },
    {
        "key": "published",
        "label": "Published",
        "description": "Short has been published. Track analytics and learn what worked.",
        "exit_criteria": "Weekly analytics is entered and learnings are applied to future Shorts.",
    },
]

STAGE_KEYS = {stage["key"] for stage in PRODUCTION_STAGES}
PRIORITY_ORDER = {"urgent": 0, "high": 1, "normal": 2, "low": 3}


def _row_to_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value or default)
    except Exception:
        return default


def _latest_by_package(conn: sqlite3.Connection, table: str, columns: str = "*") -> dict[int, dict[str, Any]]:
    rows = conn.execute(
        f"""
        SELECT {columns}
        FROM {table}
        WHERE id IN (SELECT MAX(id) FROM {table} GROUP BY package_id)
        """
    ).fetchall()
    result: dict[int, dict[str, Any]] = {}
    for row in rows:
        item = dict(row)
        result[int(item["package_id"])] = item
    return result


def _derive_stage(package: dict[str, Any], related: dict[str, dict[int, dict[str, Any]]]) -> str:
    package_id = int(package["id"])
    review_status = (package.get("review_status") or "draft").lower()

    calendar = related["calendar"].get(package_id)
    approval = related["publishing_approvals"].get(package_id)
    trust = related["teacher_trust_reviews"].get(package_id)
    source = related["source_safety_reviews"].get(package_id)
    audio = related["audio_assets"].get(package_id)
    assembly = related["assembly_plans"].get(package_id)
    video = related["video_drafts"].get(package_id)
    thumbnail = related["thumbnail_guides"].get(package_id)

    if review_status == "published" or (calendar and (calendar.get("status") == "published" or calendar.get("actual_publish_date"))):
        return "published"
    if calendar and calendar.get("status") in {"planned", "scheduled"}:
        return "scheduled"
    if approval and approval.get("status") == "approved" and approval.get("reviewer_decision") == "approved":
        return "ready_to_publish"
    if approval:
        return "publishing_gate"
    if trust:
        return "teacher_review"
    if source:
        return "source_safety"
    if audio or assembly or video or thumbnail:
        return "production_assets"
    if review_status in {"edit_required", "rejected"}:
        return "script_revision"
    if review_status == "approved":
        return "production_assets"
    return "script_review"


def _read_manual_cards(conn: sqlite3.Connection) -> dict[int, dict[str, Any]]:
    rows = conn.execute("SELECT * FROM content_production_cards").fetchall()
    return {int(row["package_id"]): dict(row) for row in rows}


def _progress_score(item: dict[str, Any]) -> int:
    checks = [
        item.get("review_status") == "approved" or item.get("review_status") == "published",
        bool(item.get("audio_status")),
        bool(item.get("assembly_plan_id")),
        bool(item.get("video_draft_id")),
        bool(item.get("thumbnail_guide_id")),
        bool(item.get("source_safety_id")),
        bool(item.get("trust_review_id")),
        bool(item.get("publishing_approval_id")),
        bool(item.get("calendar_status")),
        bool(item.get("latest_analytics_id")),
    ]
    return round(sum(1 for check in checks if check) / len(checks) * 100)


def build_content_production_board(conn: sqlite3.Connection) -> dict[str, Any]:
    packages = conn.execute(
        """
        SELECT cp.id, cp.batch_id, cp.topic, cp.subject, cp.class_level, cp.language, cp.duration_seconds,
               cp.output_type, cp.tone, cp.trust_score, cp.review_status, cp.provider_used,
               cp.prompt_template_name, cp.created_at, cp.updated_at, b.name AS batch_name
        FROM content_packages cp
        LEFT JOIN content_batches b ON b.id = cp.batch_id
        ORDER BY cp.id DESC
        """
    ).fetchall()

    related = {
        "calendar": {int(row["package_id"]): dict(row) for row in conn.execute("SELECT * FROM publishing_calendar").fetchall()},
        "publishing_approvals": _latest_by_package(conn, "publishing_approvals"),
        "teacher_trust_reviews": _latest_by_package(conn, "teacher_trust_reviews"),
        "source_safety_reviews": _latest_by_package(conn, "source_safety_reviews"),
        "audio_assets": _latest_by_package(conn, "audio_assets"),
        "assembly_plans": _latest_by_package(conn, "assembly_plans"),
        "video_drafts": _latest_by_package(conn, "video_drafts"),
        "thumbnail_guides": _latest_by_package(conn, "thumbnail_guides"),
        "manual_analytics": _latest_by_package(conn, "manual_analytics"),
    }
    manual_cards = _read_manual_cards(conn)

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cards: list[dict[str, Any]] = []

    for row in packages:
        package = dict(row)
        package_id = int(package["id"])
        manual = manual_cards.get(package_id, {})
        derived_stage = _derive_stage(package, related)
        manual_stage = manual.get("stage") or ""
        stage = manual_stage if manual_stage in STAGE_KEYS else derived_stage

        calendar = related["calendar"].get(package_id, {})
        approval = related["publishing_approvals"].get(package_id, {})
        trust = related["teacher_trust_reviews"].get(package_id, {})
        source = related["source_safety_reviews"].get(package_id, {})
        audio = related["audio_assets"].get(package_id, {})
        assembly = related["assembly_plans"].get(package_id, {})
        video = related["video_drafts"].get(package_id, {})
        thumbnail = related["thumbnail_guides"].get(package_id, {})
        analytics = related["manual_analytics"].get(package_id, {})

        card = {
            **package,
            "stage": stage,
            "derived_stage": derived_stage,
            "manual_stage_override": bool(manual_stage),
            "priority": manual.get("priority") or "normal",
            "owner": manual.get("owner") or "",
            "due_date": manual.get("due_date") or "",
            "board_notes": manual.get("notes") or "",
            "calendar_status": calendar.get("status") or "",
            "planned_publish_date": calendar.get("planned_publish_date") or "",
            "actual_publish_date": calendar.get("actual_publish_date") or "",
            "publishing_approval_id": approval.get("id"),
            "publishing_approval_status": approval.get("status") or "",
            "source_safety_id": source.get("id"),
            "source_safety_risk": source.get("risk_level") or "",
            "trust_review_id": trust.get("id"),
            "overall_trust_score": _safe_int(trust.get("overall_trust_score"), _safe_int(package.get("trust_score"))),
            "audio_status": audio.get("status") or "",
            "assembly_plan_id": assembly.get("id"),
            "video_draft_id": video.get("id"),
            "thumbnail_guide_id": thumbnail.get("id"),
            "latest_analytics_id": analytics.get("id"),
            "latest_views": _safe_int(analytics.get("views")),
            "latest_retention_pct": float(analytics.get("retention_pct") or 0),
        }
        card["progress_score"] = _progress_score(card)
        grouped[stage].append(card)
        cards.append(card)

    for items in grouped.values():
        items.sort(key=lambda item: (PRIORITY_ORDER.get(item.get("priority", "normal"), 2), item.get("due_date") or "9999-12-31", -int(item["id"])))

    stage_summaries = []
    for stage in PRODUCTION_STAGES:
        items = grouped.get(stage["key"], [])
        stage_summaries.append({
            **stage,
            "count": len(items),
            "avg_progress": round(sum(item["progress_score"] for item in items) / len(items), 1) if items else 0,
            "cards": items,
        })

    priorities = defaultdict(int)
    for card in cards:
        priorities[card["priority"]] += 1

    return {
        "generated_on": date.today().isoformat(),
        "stages": stage_summaries,
        "cards": cards,
        "summary": {
            "total_cards": len(cards),
            "blocked_or_revision": len(grouped.get("script_revision", [])) + len(grouped.get("publishing_gate", [])),
            "ready_or_scheduled": len(grouped.get("ready_to_publish", [])) + len(grouped.get("scheduled", [])),
            "published": len(grouped.get("published", [])),
            "priority_counts": dict(priorities),
        },
        "recommendations": _board_recommendations(stage_summaries),
    }


def _board_recommendations(stage_summaries: list[dict[str, Any]]) -> list[str]:
    by_key = {stage["key"]: stage for stage in stage_summaries}
    recs: list[str] = []
    if by_key["script_review"]["count"] > 5:
        recs.append("Script review has many items. Review/edit a small batch before generating more packages.")
    if by_key["production_assets"]["count"] > 0:
        recs.append("Generate narration, assembly plans, thumbnails, and video drafts for production asset cards.")
    if by_key["source_safety"]["count"] > 0:
        recs.append("Finish source safety checks before trust review and publishing approval.")
    if by_key["ready_to_publish"]["count"] > 0:
        recs.append("Move ready-to-publish Shorts into the calendar so weekly publishing stays consistent.")
    if by_key["published"]["count"] > 0:
        recs.append("Enter analytics for published Shorts weekly and use the insights page to choose the next batch.")
    if not recs:
        recs.append("Create or seed packages to start using the production board.")
    return recs


def update_production_card(
    conn: sqlite3.Connection,
    package_id: int,
    *,
    stage: str,
    priority: str = "normal",
    owner: str = "",
    due_date: str = "",
    notes: str = "",
) -> dict[str, Any]:
    if stage not in STAGE_KEYS:
        raise ValueError(f"Unknown production stage: {stage}")
    if priority not in {"urgent", "high", "normal", "low"}:
        raise ValueError("Priority must be urgent, high, normal, or low")

    existing = conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone()
    if existing is None:
        raise ValueError("Package not found")

    conn.execute(
        """
        INSERT INTO content_production_cards (package_id, stage, priority, owner, due_date, notes, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(package_id) DO UPDATE SET
            stage = excluded.stage,
            priority = excluded.priority,
            owner = excluded.owner,
            due_date = excluded.due_date,
            notes = excluded.notes,
            updated_at = CURRENT_TIMESTAMP
        """,
        (package_id, stage, priority, owner, due_date, notes),
    )
    row = conn.execute("SELECT * FROM content_production_cards WHERE package_id = ?", (package_id,)).fetchone()
    return dict(row)


def build_content_production_board_markdown(board: dict[str, Any]) -> str:
    lines = [
        "# Content Production Board",
        "",
        f"Generated on: {board.get('generated_on', '')}",
        "",
        "## Summary",
        "",
        f"- Total cards: {board['summary']['total_cards']}",
        f"- Blocked/revision: {board['summary']['blocked_or_revision']}",
        f"- Ready or scheduled: {board['summary']['ready_or_scheduled']}",
        f"- Published: {board['summary']['published']}",
        "",
        "## Recommendations",
        "",
    ]
    lines.extend([f"- {item}" for item in board.get("recommendations", [])])
    lines.append("")
    for stage in board["stages"]:
        lines.extend([f"## {stage['label']} ({stage['count']})", "", stage["description"], ""])
        if not stage["cards"]:
            lines.extend(["No cards in this stage.", ""])
            continue
        for card in stage["cards"]:
            lines.extend([
                f"### #{card['id']} — {card['topic']}",
                f"- Subject: {card['subject']} / {card['class_level']}",
                f"- Priority: {card['priority']}",
                f"- Owner: {card['owner'] or '-'}",
                f"- Due date: {card['due_date'] or '-'}",
                f"- Progress: {card['progress_score']}%",
                f"- Review status: {card['review_status']}",
                f"- Batch: {card.get('batch_name') or '-'}",
                f"- Calendar: {card.get('calendar_status') or '-'} {card.get('planned_publish_date') or ''}".strip(),
                f"- Notes: {card['board_notes'] or '-'}",
                "",
            ])
    return "\n".join(lines)
