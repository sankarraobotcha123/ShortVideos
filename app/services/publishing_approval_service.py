from __future__ import annotations

import json
from typing import Any, Mapping


REQUIRED_CHECKS = {
    "script_review_approved",
    "source_safety_generated",
    "source_safety_not_high_risk",
    "teacher_trust_generated",
    "teacher_trust_score_ready",
    "content_not_rejected",
}

APPROVAL_DECISIONS = {"pending", "approved", "changes_required", "rejected"}


def _row_to_dict(row: Any) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _latest(conn, table: str, package_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        f"SELECT * FROM {table} WHERE package_id = ? ORDER BY id DESC LIMIT 1",
        (package_id,),
    ).fetchone()
    return _row_to_dict(row)


def _count(conn, table: str, package_id: int) -> int:
    return int(conn.execute(f"SELECT COUNT(*) AS count FROM {table} WHERE package_id = ?", (package_id,)).fetchone()["count"] or 0)


def _check(key: str, label: str, passed: bool, required: bool, detail: str) -> dict[str, Any]:
    return {
        "key": key,
        "label": label,
        "passed": bool(passed),
        "required": bool(required),
        "detail": detail,
    }


def build_publishing_gate(conn, package_id: int) -> dict[str, Any]:
    package = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
    if package is None:
        raise ValueError("Package not found")
    package = dict(package)

    source_safety = _latest(conn, "source_safety_reviews", package_id)
    trust_review = _latest(conn, "teacher_trust_reviews", package_id)
    thumbnail_count = _count(conn, "thumbnail_guides", package_id)
    audio_count = _count(conn, "audio_assets", package_id)
    assembly_count = _count(conn, "assembly_plans", package_id)
    video_draft_count = _count(conn, "video_drafts", package_id)
    learning_count = _count(conn, "learning_outputs", package_id)
    calendar = conn.execute("SELECT * FROM publishing_calendar WHERE package_id = ?", (package_id,)).fetchone()
    calendar = _row_to_dict(calendar)

    review_status = package.get("review_status") or "draft"
    source_risk = (source_safety or {}).get("risk_level", "missing")
    source_decision = (source_safety or {}).get("reviewer_decision", "pending")
    trust_score = int((trust_review or {}).get("overall_trust_score") or package.get("trust_score") or 0)
    trust_decision = (trust_review or {}).get("reviewer_decision", "pending")

    checklist = [
        _check(
            "script_review_approved",
            "Script review approved",
            review_status in {"approved", "published"},
            True,
            f"Current package review status is '{review_status}'.",
        ),
        _check(
            "source_safety_generated",
            "Source safety review generated",
            source_safety is not None,
            True,
            "Latest source safety review found." if source_safety else "Generate a source safety/originality review before publishing.",
        ),
        _check(
            "source_safety_not_high_risk",
            "Source safety risk is not high",
            bool(source_safety) and source_risk in {"low", "medium"},
            True,
            f"Latest source safety risk is '{source_risk}'.",
        ),
        _check(
            "content_not_rejected",
            "No reviewer rejection on safety/trust checks",
            source_decision not in {"rejected"} and trust_decision not in {"rejected", "rewrite_required"},
            True,
            f"Source decision: {source_decision}; trust decision: {trust_decision}.",
        ),
        _check(
            "teacher_trust_generated",
            "Teacher Trust Score review generated",
            trust_review is not None,
            True,
            "Latest Teacher Trust Score review found." if trust_review else "Generate a Teacher Trust Score review before publishing.",
        ),
        _check(
            "teacher_trust_score_ready",
            "Teacher Trust Score is publish-ready",
            trust_score >= 85,
            True,
            f"Latest trust score is {trust_score}. Required: 85+.",
        ),
        _check(
            "thumbnail_ready",
            "Thumbnail helper generated",
            thumbnail_count > 0,
            False,
            f"Thumbnail guides: {thumbnail_count}. Recommended before publishing.",
        ),
        _check(
            "assembly_ready",
            "Assembly plan generated",
            assembly_count > 0,
            False,
            f"Assembly plans: {assembly_count}. Recommended for repeatable editing.",
        ),
        _check(
            "audio_ready",
            "Narration asset or recording guide exists",
            audio_count > 0,
            False,
            f"Narration assets/guides: {audio_count}. Recommended before final edit.",
        ),
        _check(
            "video_draft_ready",
            "Vertical MP4 draft generated",
            video_draft_count > 0,
            False,
            f"Video drafts: {video_draft_count}. Useful for review before final CapCut edit.",
        ),
        _check(
            "learning_outputs_ready",
            "Learning outputs generated",
            learning_count > 0,
            False,
            f"Learning output packs: {learning_count}. Useful for future monetization/products.",
        ),
        _check(
            "calendar_scheduled",
            "Publishing calendar entry exists",
            calendar is not None,
            False,
            "Calendar entry found." if calendar else "Schedule this Short after approval.",
        ),
    ]

    required_failures = [item for item in checklist if item["required"] and not item["passed"]]
    optional_warnings = [item for item in checklist if not item["required"] and not item["passed"]]
    gate_status = "approved" if not required_failures else "blocked"
    recommendation = (
        "Required checks passed. A publisher can approve this package for publishing."
        if gate_status == "approved"
        else "Do not publish yet. Fix required checklist items, regenerate the gate, then approve."
    )

    report_markdown = build_publishing_gate_markdown(
        package=package,
        checklist=checklist,
        gate_status=gate_status,
        recommendation=recommendation,
        required_failures=required_failures,
        optional_warnings=optional_warnings,
    )

    return {
        "package_id": package_id,
        "topic": package.get("topic", ""),
        "gate_status": gate_status,
        "required_failures_count": len(required_failures),
        "optional_warnings_count": len(optional_warnings),
        "checklist": checklist,
        "recommendation": recommendation,
        "report_markdown": report_markdown,
    }


def build_publishing_gate_markdown(
    *,
    package: Mapping[str, Any],
    checklist: list[dict[str, Any]],
    gate_status: str,
    recommendation: str,
    required_failures: list[dict[str, Any]],
    optional_warnings: list[dict[str, Any]],
) -> str:
    lines = [
        f"# Publishing Approval Gate: {package.get('topic', 'Content Package')}",
        "",
        f"- Package ID: {package.get('id')}",
        f"- Subject: {package.get('subject', '')}",
        f"- Class/Level: {package.get('class_level', '')}",
        f"- Duration: {package.get('duration_seconds', '')} seconds",
        f"- Gate Status: **{gate_status.upper()}**",
        "",
        "## Recommendation",
        "",
        recommendation,
        "",
        "## Required failures",
        "",
    ]
    if required_failures:
        lines.extend(f"- {item['label']}: {item['detail']}" for item in required_failures)
    else:
        lines.append("- None. Required checks passed.")
    lines.extend(["", "## Optional warnings", ""])
    if optional_warnings:
        lines.extend(f"- {item['label']}: {item['detail']}" for item in optional_warnings)
    else:
        lines.append("- None. Optional workflow checks are complete.")
    lines.extend(["", "## Full checklist", ""])
    for item in checklist:
        mark = "✅" if item["passed"] else "❌"
        required = "required" if item["required"] else "recommended"
        lines.append(f"- {mark} **{item['label']}** ({required}) — {item['detail']}")
    lines.extend([
        "",
        "## Publisher rule",
        "",
        "Only mark this Short as published after the gate status is approved and a publisher has added an approval decision.",
    ])
    return "\n".join(lines) + "\n"


def create_publishing_approval(conn, package_id: int, reviewer_name: str = "") -> dict[str, Any]:
    gate = build_publishing_gate(conn, package_id)
    status = "needs_publisher_approval" if gate["gate_status"] == "approved" else "blocked"
    cursor = conn.execute(
        """
        INSERT INTO publishing_approvals (
            package_id, status, gate_status, required_failures_count, optional_warnings_count,
            checklist_json, recommendation, report_markdown, reviewer_decision,
            reviewer_name, reviewer_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, '')
        """,
        (
            package_id,
            status,
            gate["gate_status"],
            gate["required_failures_count"],
            gate["optional_warnings_count"],
            json.dumps(gate["checklist"], ensure_ascii=False),
            gate["recommendation"],
            gate["report_markdown"],
            reviewer_name,
        ),
    )
    return get_publishing_approval(conn, int(cursor.lastrowid))


def get_publishing_approval(conn, approval_id: int) -> dict[str, Any] | None:
    row = conn.execute("SELECT * FROM publishing_approvals WHERE id = ?", (approval_id,)).fetchone()
    if row is None:
        return None
    item = dict(row)
    try:
        item["checklist"] = json.loads(item.get("checklist_json") or "[]")
    except Exception:
        item["checklist"] = []
    return item


def list_publishing_approvals(conn, package_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM publishing_approvals WHERE package_id = ? ORDER BY id DESC",
        (package_id,),
    ).fetchall()
    return [get_publishing_approval(conn, int(row["id"])) for row in rows]


def update_publishing_approval_decision(
    conn,
    approval_id: int,
    *,
    reviewer_decision: str,
    reviewer_name: str = "",
    reviewer_notes: str = "",
) -> dict[str, Any]:
    if reviewer_decision not in APPROVAL_DECISIONS:
        raise ValueError("Invalid publisher decision")
    existing = get_publishing_approval(conn, approval_id)
    if existing is None:
        raise ValueError("Publishing approval not found")

    gate_status = existing.get("gate_status")
    if reviewer_decision == "approved" and gate_status != "approved":
        status = "blocked"
        reviewer_notes = (reviewer_notes or "") + "\nApproval was not applied because required gate checks are still blocked."
    elif reviewer_decision == "approved":
        status = "approved"
    elif reviewer_decision == "changes_required":
        status = "changes_required"
    elif reviewer_decision == "rejected":
        status = "rejected"
    else:
        status = "needs_publisher_approval" if gate_status == "approved" else "blocked"

    conn.execute(
        """
        UPDATE publishing_approvals
           SET status = ?, reviewer_decision = ?, reviewer_name = ?, reviewer_notes = ?, updated_at = CURRENT_TIMESTAMP
         WHERE id = ?
        """,
        (status, reviewer_decision, reviewer_name.strip(), reviewer_notes.strip(), approval_id),
    )
    return get_publishing_approval(conn, approval_id)


def has_approved_publishing_gate(conn, package_id: int) -> bool:
    row = conn.execute(
        """
        SELECT id FROM publishing_approvals
        WHERE package_id = ? AND status = 'approved' AND reviewer_decision = 'approved'
        ORDER BY id DESC LIMIT 1
        """,
        (package_id,),
    ).fetchone()
    return row is not None
