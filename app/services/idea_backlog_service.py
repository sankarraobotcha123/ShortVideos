from __future__ import annotations

import json
from typing import Any

IDEA_STATUSES = ["backlog", "shortlisted", "ready", "converted", "archived"]
IDEA_TYPES = ["curiosity", "textbook_doubt", "exam_friendly", "myth_vs_fact", "mistake_correction", "series"]


def clamp_score(value: Any, default: int = 5) -> int:
    try:
        number = int(value)
    except Exception:
        number = default
    return max(1, min(10, number))


def calculate_topic_score(
    *,
    curiosity_score: int,
    evergreen_score: int,
    visual_potential_score: int,
    student_value_score: int,
    production_effort_score: int,
    monetization_potential_score: int,
) -> dict[str, Any]:
    """Return a practical Shorts-first topic score out of 100.

    Higher production effort is treated as a negative factor, because early-stage
    side-job workflow should prioritize topics that are easy to publish often.
    """
    curiosity = clamp_score(curiosity_score)
    evergreen = clamp_score(evergreen_score)
    visual = clamp_score(visual_potential_score)
    student_value = clamp_score(student_value_score)
    effort = clamp_score(production_effort_score)
    monetization = clamp_score(monetization_potential_score)
    ease = 11 - effort

    weighted = (
        curiosity * 0.25
        + evergreen * 0.18
        + visual * 0.18
        + student_value * 0.22
        + ease * 0.10
        + monetization * 0.07
    )
    total_score = round(weighted * 10, 1)
    if total_score >= 80:
        priority = "high"
        recommendation = "Strong Short idea. Move this to ready and produce soon."
    elif total_score >= 65:
        priority = "medium"
        recommendation = "Good idea. Improve the hook or visual angle before production."
    elif total_score >= 50:
        priority = "low"
        recommendation = "Keep in backlog. Use only if it supports a batch or series."
    else:
        priority = "park"
        recommendation = "Archive or rewrite. The idea may take too much effort for early Shorts output."

    return {
        "total_score": total_score,
        "priority": priority,
        "recommendation": recommendation,
        "score_breakdown": {
            "curiosity": curiosity,
            "evergreen": evergreen,
            "visual_potential": visual,
            "student_value": student_value,
            "production_effort": effort,
            "production_ease": ease,
            "monetization_potential": monetization,
        },
    }


def serialize_idea(row: Any) -> dict[str, Any]:
    idea = dict(row)
    for key in [
        "curiosity_score",
        "evergreen_score",
        "visual_potential_score",
        "student_value_score",
        "production_effort_score",
        "monetization_potential_score",
    ]:
        idea[key] = int(idea.get(key) or 0)
    idea["total_score"] = float(idea.get("total_score") or 0)
    idea["converted_package_id"] = idea.get("converted_package_id") or None
    idea["batch_id"] = idea.get("batch_id") or None
    try:
        idea["score_breakdown"] = json.loads(idea.get("score_breakdown_json") or "{}")
    except Exception:
        idea["score_breakdown"] = {}
    return idea


def list_content_ideas(conn, *, status: str | None = None, search: str = "") -> dict[str, Any]:
    clauses: list[str] = []
    params: list[Any] = []
    if status:
        clauses.append("ci.status = ?")
        params.append(status)
    if search:
        like = f"%{search.strip()}%"
        clauses.append("(ci.title LIKE ? OR ci.subject LIKE ? OR ci.hook_angle LIKE ? OR ci.notes LIKE ?)")
        params.extend([like, like, like, like])
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    rows = conn.execute(
        f"""
        SELECT ci.*, b.name AS batch_name, cp.topic AS converted_package_topic
        FROM content_ideas ci
        LEFT JOIN content_batches b ON b.id = ci.batch_id
        LEFT JOIN content_packages cp ON cp.id = ci.converted_package_id
        {where}
        ORDER BY
          CASE ci.status
            WHEN 'ready' THEN 1
            WHEN 'shortlisted' THEN 2
            WHEN 'backlog' THEN 3
            WHEN 'converted' THEN 4
            ELSE 5
          END,
          ci.total_score DESC,
          ci.updated_at DESC,
          ci.id DESC
        """,
        params,
    ).fetchall()
    ideas = [serialize_idea(row) for row in rows]
    return {"ideas": ideas, "summary": summarize_ideas(ideas)}


def summarize_ideas(ideas: list[dict[str, Any]]) -> dict[str, Any]:
    by_status: dict[str, int] = {status: 0 for status in IDEA_STATUSES}
    for idea in ideas:
        by_status[str(idea.get("status") or "backlog")] = by_status.get(str(idea.get("status") or "backlog"), 0) + 1
    ready = [idea for idea in ideas if idea.get("status") in {"ready", "shortlisted"}]
    average_score = round(sum(float(idea.get("total_score") or 0) for idea in ideas) / len(ideas), 1) if ideas else 0
    return {
        "total": len(ideas),
        "by_status": by_status,
        "ready_or_shortlisted": len(ready),
        "average_score": average_score,
        "top_idea": ideas[0] if ideas else None,
    }


def create_content_idea(conn, payload: dict[str, Any]) -> dict[str, Any]:
    scores = calculate_topic_score(
        curiosity_score=payload.get("curiosity_score", 7),
        evergreen_score=payload.get("evergreen_score", 7),
        visual_potential_score=payload.get("visual_potential_score", 7),
        student_value_score=payload.get("student_value_score", 7),
        production_effort_score=payload.get("production_effort_score", 4),
        monetization_potential_score=payload.get("monetization_potential_score", 5),
    )
    status = payload.get("status") or "backlog"
    if status not in IDEA_STATUSES:
        raise ValueError("Invalid idea status")
    idea_type = payload.get("idea_type") or "curiosity"
    cursor = conn.execute(
        """
        INSERT INTO content_ideas (
            title, subject, class_level, target_audience, language, idea_type, hook_angle,
            source_hint, batch_id, status, notes, curiosity_score, evergreen_score,
            visual_potential_score, student_value_score, production_effort_score,
            monetization_potential_score, total_score, priority, recommendation, score_breakdown_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload.get("title", "").strip(),
            payload.get("subject", "Science").strip(),
            payload.get("class_level", "Class 7").strip(),
            payload.get("target_audience", "School students").strip(),
            payload.get("language", "English").strip(),
            idea_type.strip(),
            payload.get("hook_angle", "").strip(),
            payload.get("source_hint", "").strip(),
            payload.get("batch_id") or None,
            status,
            payload.get("notes", "").strip(),
            scores["score_breakdown"]["curiosity"],
            scores["score_breakdown"]["evergreen"],
            scores["score_breakdown"]["visual_potential"],
            scores["score_breakdown"]["student_value"],
            scores["score_breakdown"]["production_effort"],
            scores["score_breakdown"]["monetization_potential"],
            scores["total_score"],
            scores["priority"],
            scores["recommendation"],
            json.dumps(scores["score_breakdown"]),
        ),
    )
    return get_content_idea(conn, int(cursor.lastrowid))


def get_content_idea(conn, idea_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT ci.*, b.name AS batch_name, cp.topic AS converted_package_topic
        FROM content_ideas ci
        LEFT JOIN content_batches b ON b.id = ci.batch_id
        LEFT JOIN content_packages cp ON cp.id = ci.converted_package_id
        WHERE ci.id = ?
        """,
        (idea_id,),
    ).fetchone()
    return serialize_idea(row) if row else None


def update_content_idea(conn, idea_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    existing = get_content_idea(conn, idea_id)
    if existing is None:
        raise ValueError("Content idea not found")
    merged = {**existing, **payload}
    scores = calculate_topic_score(
        curiosity_score=merged.get("curiosity_score", 7),
        evergreen_score=merged.get("evergreen_score", 7),
        visual_potential_score=merged.get("visual_potential_score", 7),
        student_value_score=merged.get("student_value_score", 7),
        production_effort_score=merged.get("production_effort_score", 4),
        monetization_potential_score=merged.get("monetization_potential_score", 5),
    )
    status = merged.get("status") or "backlog"
    if status not in IDEA_STATUSES:
        raise ValueError("Invalid idea status")
    conn.execute(
        """
        UPDATE content_ideas
        SET title = ?, subject = ?, class_level = ?, target_audience = ?, language = ?, idea_type = ?,
            hook_angle = ?, source_hint = ?, batch_id = ?, status = ?, notes = ?,
            curiosity_score = ?, evergreen_score = ?, visual_potential_score = ?, student_value_score = ?,
            production_effort_score = ?, monetization_potential_score = ?, total_score = ?, priority = ?,
            recommendation = ?, score_breakdown_json = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            str(merged.get("title") or "").strip(),
            str(merged.get("subject") or "Science").strip(),
            str(merged.get("class_level") or "Class 7").strip(),
            str(merged.get("target_audience") or "School students").strip(),
            str(merged.get("language") or "English").strip(),
            str(merged.get("idea_type") or "curiosity").strip(),
            str(merged.get("hook_angle") or "").strip(),
            str(merged.get("source_hint") or "").strip(),
            merged.get("batch_id") or None,
            status,
            str(merged.get("notes") or "").strip(),
            scores["score_breakdown"]["curiosity"],
            scores["score_breakdown"]["evergreen"],
            scores["score_breakdown"]["visual_potential"],
            scores["score_breakdown"]["student_value"],
            scores["score_breakdown"]["production_effort"],
            scores["score_breakdown"]["monetization_potential"],
            scores["total_score"],
            scores["priority"],
            scores["recommendation"],
            json.dumps(scores["score_breakdown"]),
            idea_id,
        ),
    )
    return get_content_idea(conn, idea_id) or {}


def mark_idea_converted(conn, idea_id: int, package_id: int) -> dict[str, Any]:
    conn.execute(
        """
        UPDATE content_ideas
        SET status = 'converted', converted_package_id = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (package_id, idea_id),
    )
    return get_content_idea(conn, idea_id) or {}


def build_content_ideas_markdown(ideas_payload: dict[str, Any]) -> str:
    ideas = ideas_payload.get("ideas", [])
    summary = ideas_payload.get("summary", {})
    lines = [
        "# Content Idea Backlog",
        "",
        f"Total ideas: {summary.get('total', 0)}",
        f"Average score: {summary.get('average_score', 0)}",
        f"Ready/shortlisted: {summary.get('ready_or_shortlisted', 0)}",
        "",
        "## Ideas",
        "",
    ]
    for idea in ideas:
        lines.extend(
            [
                f"### #{idea.get('id')} - {idea.get('title')}",
                f"- Status: {idea.get('status')}",
                f"- Score: {idea.get('total_score')} ({idea.get('priority')})",
                f"- Subject/Level: {idea.get('subject')} / {idea.get('class_level')}",
                f"- Type: {idea.get('idea_type')}",
                f"- Hook angle: {idea.get('hook_angle') or '-'}",
                f"- Recommendation: {idea.get('recommendation')}",
                f"- Notes: {idea.get('notes') or '-'}",
                "",
            ]
        )
    return "\n".join(lines)
