from __future__ import annotations

import json
from typing import Any

LANGUAGE_PLAN_STATUSES = [
    "planning",
    "ready_for_translation",
    "translated",
    "voice_review",
    "published",
    "blocked",
]

SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "Kannada",
    "Malayalam",
    "Marathi",
    "Bengali",
]

VOICE_STRATEGIES = ["manual_voice", "local_tts", "browser_preview", "future_paid_tts"]
SUBTITLE_STRATEGIES = ["manual_review", "direct_translation", "bilingual_subtitles", "future_ai_translation"]


def _clean_text(value: Any, default: str = "") -> str:
    return str(value if value is not None else default).strip()


def _bool(value: Any) -> bool:
    return bool(int(value)) if isinstance(value, int) else bool(value)


def _row_to_plan(row: Any) -> dict[str, Any]:
    plan = dict(row)
    plan["needs_human_translation_review"] = bool(plan.get("needs_human_translation_review"))
    try:
        plan["checklist"] = json.loads(plan.get("checklist_json") or "[]")
    except Exception:
        plan["checklist"] = []
    return plan


def _build_checklist(payload: dict[str, Any]) -> list[dict[str, Any]]:
    target_language = _clean_text(payload.get("target_language"))
    cultural_notes = _clean_text(payload.get("cultural_notes"))
    glossary_terms = _clean_text(payload.get("glossary_terms"))
    voice_strategy = _clean_text(payload.get("voice_strategy"))
    subtitle_strategy = _clean_text(payload.get("subtitle_strategy"))
    reviewer = _clean_text(payload.get("reviewer_name"))
    return [
        {"label": "Target language selected", "passed": bool(target_language), "fix": "Choose a target language before translation."},
        {"label": "Cultural notes added", "passed": bool(cultural_notes), "fix": "Add language-specific examples, words to avoid, or regional notes."},
        {"label": "Glossary terms prepared", "passed": bool(glossary_terms), "fix": "Add key terms that must stay accurate in translation."},
        {"label": "Voice strategy selected", "passed": voice_strategy in VOICE_STRATEGIES, "fix": "Choose manual voice, local TTS, browser preview, or future paid TTS."},
        {"label": "Subtitle strategy selected", "passed": subtitle_strategy in SUBTITLE_STRATEGIES, "fix": "Choose how subtitles will be reviewed or translated."},
        {"label": "Reviewer assigned", "passed": bool(reviewer), "fix": "Add the person who will review the translated version."},
    ]


def _readiness_score(checklist: list[dict[str, Any]], needs_review: bool) -> int:
    if not checklist:
        return 0
    passed = sum(1 for item in checklist if item.get("passed"))
    score = round((passed / len(checklist)) * 100)
    if needs_review:
        score = max(score - 5, 0)
    return int(score)


def _recommendation(score: int, status: str) -> str:
    if status == "blocked":
        return "Blocked. Resolve notes before using this language in production."
    if score >= 85:
        return "Ready for translation/recording workflow. Still do a final human language review before publishing."
    if score >= 65:
        return "Usable plan, but add missing glossary, cultural notes, or reviewer details before translation."
    return "Not ready. Complete the missing multilingual planning fields first."


def create_multilingual_plan(conn, payload: dict[str, Any]) -> dict[str, Any]:
    package_id = payload.get("package_id") or None
    if package_id:
        package = conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        if package is None:
            raise ValueError("Package not found")
    source_language = _clean_text(payload.get("source_language"), "English") or "English"
    target_language = _clean_text(payload.get("target_language"), "Hindi") or "Hindi"
    if source_language.lower() == target_language.lower():
        raise ValueError("Target language must be different from source language")
    status = _clean_text(payload.get("status"), "planning") or "planning"
    if status not in LANGUAGE_PLAN_STATUSES:
        raise ValueError(f"Invalid multilingual plan status: {status}")
    voice_strategy = _clean_text(payload.get("voice_strategy"), "manual_voice") or "manual_voice"
    subtitle_strategy = _clean_text(payload.get("subtitle_strategy"), "manual_review") or "manual_review"
    needs_review = _bool(payload.get("needs_human_translation_review", True))
    normalized = {
        "package_id": package_id,
        "source_language": source_language,
        "target_language": target_language,
        "status": status,
        "priority": _clean_text(payload.get("priority"), "medium") or "medium",
        "translation_goal": _clean_text(payload.get("translation_goal"), "Make this Short understandable for local-language students without changing the science meaning."),
        "cultural_notes": _clean_text(payload.get("cultural_notes")),
        "glossary_terms": _clean_text(payload.get("glossary_terms")),
        "voice_strategy": voice_strategy if voice_strategy in VOICE_STRATEGIES else "manual_voice",
        "subtitle_strategy": subtitle_strategy if subtitle_strategy in SUBTITLE_STRATEGIES else "manual_review",
        "reviewer_name": _clean_text(payload.get("reviewer_name")),
        "notes": _clean_text(payload.get("notes")),
        "needs_human_translation_review": 1 if needs_review else 0,
    }
    checklist = _build_checklist(normalized)
    readiness_score = _readiness_score(checklist, needs_review)
    recommendation = _recommendation(readiness_score, status)
    cursor = conn.execute(
        """
        INSERT INTO multilingual_plans (
            package_id, source_language, target_language, status, priority,
            translation_goal, cultural_notes, glossary_terms, voice_strategy,
            subtitle_strategy, reviewer_name, notes, needs_human_translation_review,
            readiness_score, recommendation, checklist_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            normalized["package_id"], normalized["source_language"], normalized["target_language"], normalized["status"], normalized["priority"],
            normalized["translation_goal"], normalized["cultural_notes"], normalized["glossary_terms"], normalized["voice_strategy"],
            normalized["subtitle_strategy"], normalized["reviewer_name"], normalized["notes"], normalized["needs_human_translation_review"],
            readiness_score, recommendation, json.dumps(checklist, ensure_ascii=False),
        ),
    )
    return get_multilingual_plan(conn, cursor.lastrowid)


def update_multilingual_plan(conn, plan_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    existing = get_multilingual_plan(conn, plan_id)
    if existing is None:
        raise ValueError("Multilingual plan not found")
    merged = dict(existing)
    merged.update({key: value for key, value in payload.items() if value is not None})
    package_id = merged.get("package_id") or None
    if package_id:
        package = conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        if package is None:
            raise ValueError("Package not found")
    if str(merged.get("source_language", "")).lower() == str(merged.get("target_language", "")).lower():
        raise ValueError("Target language must be different from source language")
    status = _clean_text(merged.get("status"), "planning") or "planning"
    if status not in LANGUAGE_PLAN_STATUSES:
        raise ValueError(f"Invalid multilingual plan status: {status}")
    checklist = _build_checklist(merged)
    needs_review = _bool(merged.get("needs_human_translation_review", True))
    readiness_score = _readiness_score(checklist, needs_review)
    recommendation = _recommendation(readiness_score, status)
    conn.execute(
        """
        UPDATE multilingual_plans
           SET package_id = ?, source_language = ?, target_language = ?, status = ?, priority = ?,
               translation_goal = ?, cultural_notes = ?, glossary_terms = ?, voice_strategy = ?,
               subtitle_strategy = ?, reviewer_name = ?, notes = ?, needs_human_translation_review = ?,
               readiness_score = ?, recommendation = ?, checklist_json = ?, updated_at = CURRENT_TIMESTAMP
         WHERE id = ?
        """,
        (
            package_id,
            _clean_text(merged.get("source_language"), "English") or "English",
            _clean_text(merged.get("target_language"), "Hindi") or "Hindi",
            status,
            _clean_text(merged.get("priority"), "medium") or "medium",
            _clean_text(merged.get("translation_goal")),
            _clean_text(merged.get("cultural_notes")),
            _clean_text(merged.get("glossary_terms")),
            _clean_text(merged.get("voice_strategy"), "manual_voice") or "manual_voice",
            _clean_text(merged.get("subtitle_strategy"), "manual_review") or "manual_review",
            _clean_text(merged.get("reviewer_name")),
            _clean_text(merged.get("notes")),
            1 if needs_review else 0,
            readiness_score,
            recommendation,
            json.dumps(checklist, ensure_ascii=False),
            plan_id,
        ),
    )
    return get_multilingual_plan(conn, plan_id)


def get_multilingual_plan(conn, plan_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT mp.*, cp.topic AS package_topic, cp.subject AS package_subject, cp.class_level AS package_class_level
          FROM multilingual_plans mp
          LEFT JOIN content_packages cp ON cp.id = mp.package_id
         WHERE mp.id = ?
        """,
        (plan_id,),
    ).fetchone()
    return _row_to_plan(row) if row else None


def list_multilingual_plans(conn, target_language: str = "", status: str = "") -> dict[str, Any]:
    conditions: list[str] = []
    params: list[Any] = []
    if target_language:
        conditions.append("LOWER(mp.target_language) = LOWER(?)")
        params.append(target_language)
    if status:
        conditions.append("mp.status = ?")
        params.append(status)
    where_sql = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    rows = conn.execute(
        f"""
        SELECT mp.*, cp.topic AS package_topic, cp.subject AS package_subject, cp.class_level AS package_class_level
          FROM multilingual_plans mp
          LEFT JOIN content_packages cp ON cp.id = mp.package_id
          {where_sql}
         ORDER BY
              CASE mp.priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 WHEN 'low' THEN 3 ELSE 4 END,
              mp.updated_at DESC,
              mp.id DESC
        """,
        params,
    ).fetchall()
    plans = [_row_to_plan(row) for row in rows]
    return {
        "plans": plans,
        "statuses": LANGUAGE_PLAN_STATUSES,
        "supported_languages": SUPPORTED_LANGUAGES,
        "voice_strategies": VOICE_STRATEGIES,
        "subtitle_strategies": SUBTITLE_STRATEGIES,
        "summary": build_multilingual_summary(plans),
    }


def build_multilingual_summary(plans: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(plans)
    by_language: dict[str, int] = {}
    by_status: dict[str, int] = {}
    ready = 0
    needs_review = 0
    for plan in plans:
        by_language[plan.get("target_language") or "Unknown"] = by_language.get(plan.get("target_language") or "Unknown", 0) + 1
        by_status[plan.get("status") or "planning"] = by_status.get(plan.get("status") or "planning", 0) + 1
        if int(plan.get("readiness_score") or 0) >= 85:
            ready += 1
        if plan.get("needs_human_translation_review"):
            needs_review += 1
    return {"total": total, "ready_count": ready, "needs_review_count": needs_review, "by_language": by_language, "by_status": by_status}


def build_multilingual_plans_markdown(payload: dict[str, Any]) -> str:
    plans = payload.get("plans", [])
    summary = payload.get("summary", {})
    lines = [
        "# Multilingual Planning Report",
        "",
        f"- Total plans: {summary.get('total', 0)}",
        f"- Ready plans: {summary.get('ready_count', 0)}",
        f"- Plans needing human review: {summary.get('needs_review_count', 0)}",
        "",
        "## Language Summary",
        "",
    ]
    for language, count in (summary.get("by_language") or {}).items():
        lines.append(f"- {language}: {count}")
    if not (summary.get("by_language") or {}):
        lines.append("- No multilingual plans yet.")
    lines.extend(["", "## Plans", ""])
    for plan in plans:
        lines.extend([
            f"### #{plan.get('id')} — {plan.get('target_language')}",
            "",
            f"- Package: {plan.get('package_topic') or 'Standalone plan'}",
            f"- Source language: {plan.get('source_language')}",
            f"- Status: {plan.get('status')}",
            f"- Priority: {plan.get('priority')}",
            f"- Readiness score: {plan.get('readiness_score')}",
            f"- Voice strategy: {plan.get('voice_strategy')}",
            f"- Subtitle strategy: {plan.get('subtitle_strategy')}",
            f"- Reviewer: {plan.get('reviewer_name') or 'Not assigned'}",
            f"- Recommendation: {plan.get('recommendation')}",
            "",
            "Checklist:",
        ])
        for item in plan.get("checklist", []):
            mark = "✅" if item.get("passed") else "⚠️"
            lines.append(f"- {mark} {item.get('label')} — {item.get('fix', '')}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
