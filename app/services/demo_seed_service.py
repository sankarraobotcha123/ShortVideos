from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.services.content_generator import ContentInput
from app.services.generation_orchestrator import generate_content_package_with_fallbacks, provider_status
from app.services.learning_output_service import generate_learning_output
from app.services.provider_log_service import record_generation_provider_logs
from app.services.prompt_template_service import apply_script_prompt_template, list_prompt_templates, seed_default_prompt_templates
from app.services.source_safety_service import generate_source_safety_review
from app.services.thumbnail_service import generate_thumbnail_guide
from app.services.trust_score_service import build_trust_review

DEMO_BATCH_NAME = "Demo Batch - First Science Curiosity Shorts"
DEMO_SOURCE_NAME = "Demo seed data"

DEMO_TOPICS: list[dict[str, Any]] = [
    {
        "topic": "Why are leaves green?",
        "subject": "Science",
        "tone": "Curious",
        "source_notes": "Leaves contain chlorophyll. Chlorophyll absorbs sunlight and helps plants make food through photosynthesis. Chlorophyll reflects green light, so leaves look green.",
        "template_style": "curiosity",
        "views": 1280,
        "likes": 86,
        "comments": 9,
        "shares": 14,
        "retention": 72.5,
        "ctr": 6.2,
    },
    {
        "topic": "Why do we see lightning before thunder?",
        "subject": "Science",
        "tone": "Mistake Correction",
        "source_notes": "Lightning and thunder happen during the same event. Light travels much faster than sound. Because light reaches our eyes before sound reaches our ears, we see lightning before hearing thunder.",
        "template_style": "mistake_correction",
        "views": 2140,
        "likes": 143,
        "comments": 18,
        "shares": 27,
        "retention": 81.0,
        "ctr": 7.8,
    },
    {
        "topic": "How does evaporation cool water?",
        "subject": "Science",
        "tone": "Exam-focused",
        "source_notes": "During evaporation, faster water molecules escape from the surface. The remaining molecules have lower average energy. Lower average energy means the water feels cooler.",
        "template_style": "exam_focused",
        "views": 760,
        "likes": 42,
        "comments": 4,
        "shares": 8,
        "retention": 58.2,
        "ctr": 4.1,
    },
]


def build_system_readiness(conn) -> dict[str, Any]:
    """Return practical run/demo checks for the React setup page."""
    counts = {
        "packages": _count(conn, "content_packages"),
        "batches": _count(conn, "content_batches"),
        "calendar_items": _count(conn, "publishing_calendar"),
        "manual_analytics": _count(conn, "manual_analytics"),
        "prompt_templates": _count(conn, "prompt_templates"),
        "provider_logs": _count(conn, "ai_provider_logs"),
    }
    dirs = [
        settings.database_path.parent,
        settings.export_dir,
        settings.audio_dir,
        settings.video_draft_dir,
        settings.asset_library_dir,
        settings.thumbnail_dir,
        settings.source_safety_dir,
        settings.trust_review_dir,
        settings.learning_output_dir,
    ]
    directory_checks = [
        {
            "path": str(path),
            "exists": path.exists(),
            "writable": _is_writable(path),
        }
        for path in dirs
    ]
    provider_checks = provider_status()
    ready_items = [
        {"label": "SQLite database folder exists", "passed": settings.database_path.parent.exists()},
        {"label": "Prompt templates seeded", "passed": counts["prompt_templates"] > 0},
        {"label": "Template AI fallback available", "passed": any(p["name"] == "template" and p["available"] for p in provider_checks)},
        {"label": "Storage folders writable", "passed": all(item["writable"] for item in directory_checks)},
        {"label": "At least one content package exists", "passed": counts["packages"] > 0},
        {"label": "Manual analytics available for insights", "passed": counts["manual_analytics"] > 0},
    ]
    return {
        "version": "0.16.0",
        "counts": counts,
        "directory_checks": directory_checks,
        "provider_checks": provider_checks,
        "ready_items": ready_items,
        "overall_ready": all(item["passed"] for item in ready_items[:4]),
        "demo_seeded": _demo_package_count(conn) > 0,
        "demo_package_count": _demo_package_count(conn),
        "recommendations": _recommendations(counts),
    }


def seed_demo_data(conn, reset_demo: bool = False) -> dict[str, Any]:
    """Seed a safe demo batch and packages for local testing.

    This is intentionally deterministic and uses only fallback/template providers,
    so it works on laptops without Ollama or Transformers. It does not delete user
    data unless reset_demo=True, and even then it deletes only rows tagged as demo.
    """
    if reset_demo:
        _delete_demo_rows(conn)

    existing_count = _demo_package_count(conn)
    if existing_count > 0 and not reset_demo:
        batch = conn.execute("SELECT * FROM content_batches WHERE name = ?", (DEMO_BATCH_NAME,)).fetchone()
        return {
            "created": False,
            "message": "Demo data already exists. Use reset_demo=true to recreate it.",
            "batch": dict(batch) if batch else None,
            "package_count": existing_count,
            "package_ids": [row[0] for row in conn.execute("SELECT id FROM content_packages WHERE source_name = ? ORDER BY id", (DEMO_SOURCE_NAME,)).fetchall()],
        }

    seed_default_prompt_templates(conn)
    templates = list_prompt_templates(conn, "script")
    template_by_style = {str(item.get("style_key") or ""): item for item in templates}

    today = date.today()
    batch_id = _create_demo_batch(conn, today)
    package_ids: list[int] = []

    for index, topic in enumerate(DEMO_TOPICS):
        template = template_by_style.get(topic["template_style"]) or (templates[0] if templates else None)
        inp = ContentInput(
            board_source="NCERT / Self-written",
            class_level="Class 7",
            subject=topic["subject"],
            topic=topic["topic"],
            audience="School students and curious learners",
            language="English",
            duration_seconds=60,
            output_type="Short",
            tone=topic["tone"],
            source_notes=topic["source_notes"],
            source_name=DEMO_SOURCE_NAME,
            source_license_type="Self-written / Demo content",
            page_or_section_reference="Demo concept notes",
            copied_text_used=False,
            transformation_notes="Demo seed converted source facts into original hook, analogy, storyboard, quiz, notes, and review workflow.",
        )
        generated = generate_content_package_with_fallbacks(inp)
        generated = apply_script_prompt_template(inp, generated, template)
        package_id = _insert_demo_package(conn, inp, generated, batch_id)
        record_generation_provider_logs(conn, package_id, generated)
        package = dict(conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone())
        _create_demo_source_safety(conn, package_id, package)
        source_reviews = [dict(row) for row in conn.execute("SELECT * FROM source_safety_reviews WHERE package_id = ? ORDER BY id DESC", (package_id,)).fetchall()]
        _create_demo_trust_review(conn, package_id, package, source_reviews)
        _create_demo_thumbnail(conn, package_id, package)
        _create_demo_learning_output(conn, package_id, package)
        _create_demo_calendar(conn, package_id, today + timedelta(days=index))
        _create_demo_analytics(conn, package_id, today + timedelta(days=index + 3), topic)
        package_ids.append(package_id)

    return {
        "created": True,
        "message": "Demo data seeded successfully.",
        "batch": dict(conn.execute("SELECT * FROM content_batches WHERE id = ?", (batch_id,)).fetchone()),
        "package_count": len(package_ids),
        "package_ids": package_ids,
    }


def _count(conn, table: str) -> int:
    row = conn.execute(f"SELECT COUNT(*) AS total FROM {table}").fetchone()
    return int(dict(row or {}).get("total") or 0)


def _demo_package_count(conn) -> int:
    row = conn.execute("SELECT COUNT(*) AS total FROM content_packages WHERE source_name = ?", (DEMO_SOURCE_NAME,)).fetchone()
    return int(dict(row or {}).get("total") or 0)


def _delete_demo_rows(conn) -> None:
    demo_ids = [row[0] for row in conn.execute("SELECT id FROM content_packages WHERE source_name = ?", (DEMO_SOURCE_NAME,)).fetchall()]
    for package_id in demo_ids:
        conn.execute("DELETE FROM content_packages WHERE id = ?", (package_id,))
    conn.execute("DELETE FROM content_batches WHERE name = ?", (DEMO_BATCH_NAME,))


def _create_demo_batch(conn, today: date) -> int:
    cursor = conn.execute(
        """
        INSERT INTO content_batches (name, niche, target_audience, start_date, end_date, planned_count, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            DEMO_BATCH_NAME,
            "Class 6-8 Science curiosity Shorts",
            "School students and curious learners",
            today.isoformat(),
            (today + timedelta(days=14)).isoformat(),
            20,
            "active",
            "Demo batch for local testing, screenshots, and review workflow validation.",
        ),
    )
    return int(cursor.lastrowid)


def _insert_demo_package(conn, inp: ContentInput, generated: dict[str, Any], batch_id: int) -> int:
    cursor = conn.execute(
        """
        INSERT INTO content_packages (
            batch_id, board_source, class_level, subject, topic, audience, language, duration_seconds,
            output_type, tone, source_notes, source_name, source_license_type,
            page_or_section_reference, copied_text_used, transformation_notes,
            hook, script_text, storyboard_markdown, subtitle_srt, visual_prompts_markdown,
            title_options, description, hashtags, quiz_question, trust_score,
            provider_used, generation_mode, provider_chain, provider_notes, provider_attempts, generation_duration_ms,
            prompt_template_id, prompt_template_name, prompt_template_style, prompt_template_snapshot,
            review_status, reviewer_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            batch_id,
            inp.board_source,
            inp.class_level,
            inp.subject,
            inp.topic,
            inp.audience,
            inp.language,
            inp.duration_seconds,
            inp.output_type,
            inp.tone,
            inp.source_notes,
            inp.source_name,
            inp.source_license_type,
            inp.page_or_section_reference,
            int(inp.copied_text_used),
            inp.transformation_notes,
            generated["hook"],
            generated["script_text"],
            generated["storyboard_markdown"],
            generated["subtitle_srt"],
            generated["visual_prompts_markdown"],
            generated["title_options"],
            generated["description"],
            generated["hashtags"],
            generated["quiz_question"],
            int(generated["trust_score"]),
            generated.get("provider_used", "template"),
            generated.get("generation_mode", "deterministic_template"),
            generated.get("provider_chain", "template"),
            generated.get("provider_notes", ""),
            generated.get("provider_attempts", "[]"),
            int(generated.get("generation_duration_ms") or 0),
            generated.get("prompt_template_id"),
            generated.get("prompt_template_name", ""),
            generated.get("prompt_template_style", ""),
            generated.get("prompt_template_snapshot", ""),
            "approved",
            "Demo seed: approved for local testing only.",
        ),
    )
    return int(cursor.lastrowid)


def _create_demo_source_safety(conn, package_id: int, package: dict[str, Any]) -> None:
    payload = generate_source_safety_review(package)
    conn.execute(
        """
        INSERT INTO source_safety_reviews (
            package_id, status, risk_level, similarity_score, sequence_similarity, keyword_overlap,
            approval_required, copied_text_used, checklist_json, recommendation, review_markdown,
            file_path, file_name, mime_type, reviewer_decision, reviewer_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            package_id,
            payload["status"],
            payload["risk_level"],
            payload["similarity_score"],
            payload["sequence_similarity"],
            payload["keyword_overlap"],
            payload["approval_required"],
            payload["copied_text_used"],
            payload["checklist_json"],
            payload["recommendation"],
            payload["review_markdown"],
            payload["file_path"],
            payload["file_name"],
            payload["mime_type"],
            "approved" if payload["risk_level"] == "low" else "pending",
            "Demo seed review.",
        ),
    )


def _create_demo_trust_review(conn, package_id: int, package: dict[str, Any], source_reviews: list[dict[str, Any]]) -> None:
    payload = build_trust_review(package, source_reviews)
    conn.execute(
        """
        INSERT INTO teacher_trust_reviews (
            package_id, status, factual_accuracy_score, age_appropriateness_score,
            simplicity_score, visual_clarity_score, engagement_score, source_safety_score,
            reviewer_confidence_score, overall_trust_score, approval_required, checklist_json,
            recommendation, reviewer_decision, reviewer_notes, file_path, file_name, mime_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            package_id,
            payload["status"],
            payload["factual_accuracy_score"],
            payload["age_appropriateness_score"],
            payload["simplicity_score"],
            payload["visual_clarity_score"],
            payload["engagement_score"],
            payload["source_safety_score"],
            payload["reviewer_confidence_score"],
            payload["overall_trust_score"],
            payload["approval_required"],
            payload["checklist_json"],
            payload["recommendation"],
            "approved" if int(payload["overall_trust_score"]) >= 85 else "edit_required",
            "Demo seed review.",
            payload["file_path"],
            payload["file_name"],
            payload["mime_type"],
        ),
    )
    conn.execute("UPDATE content_packages SET trust_score = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (payload["overall_trust_score"], package_id))


def _create_demo_thumbnail(conn, package_id: int, package: dict[str, Any]) -> None:
    payload = generate_thumbnail_guide(package)
    conn.execute(
        """
        INSERT INTO thumbnail_guides (
            package_id, status, file_path, file_name, mime_type, thumbnail_mode,
            text_ideas, layout_guide, canva_prompt, provider_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            package_id,
            payload["status"],
            payload["file_path"],
            payload["file_name"],
            payload["mime_type"],
            payload["thumbnail_mode"],
            payload["text_ideas"],
            payload["layout_guide"],
            payload["canva_prompt"],
            payload.get("provider_notes", ""),
        ),
    )


def _create_demo_learning_output(conn, package_id: int, package: dict[str, Any]) -> None:
    payload = generate_learning_output(package)
    conn.execute(
        """
        INSERT INTO learning_outputs (
            package_id, status, output_mode, revision_notes_markdown,
            flashcards_json, quiz_json, worksheet_markdown,
            file_path, file_name, mime_type, provider_notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            package_id,
            payload["status"],
            payload["output_mode"],
            payload["revision_notes_markdown"],
            payload["flashcards_json"],
            payload["quiz_json"],
            payload["worksheet_markdown"],
            payload["file_path"],
            payload["file_name"],
            payload["mime_type"],
            payload.get("provider_notes", ""),
        ),
    )


def _create_demo_calendar(conn, package_id: int, planned_date: date) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO publishing_calendar (
            package_id, planned_publish_date, actual_publish_date, platform, status, playlist_name, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            package_id,
            planned_date.isoformat(),
            "",
            "YouTube Shorts",
            "planned",
            "Science Curiosity Shorts",
            "Demo schedule entry. Replace with your real publishing date.",
        ),
    )


def _create_demo_analytics(conn, package_id: int, entry_date: date, topic: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO manual_analytics (
            package_id, platform, entry_date, views, likes, comments, shares,
            avg_view_duration_seconds, retention_pct, ctr_pct, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            package_id,
            "YouTube Shorts",
            entry_date.isoformat(),
            int(topic["views"]),
            int(topic["likes"]),
            int(topic["comments"]),
            int(topic["shares"]),
            round(60 * (float(topic["retention"]) / 100), 1),
            float(topic["retention"]),
            float(topic["ctr"]),
            "Demo analytics: replace with real Shorts performance after publishing.",
        ),
    )


def _is_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / ".write-test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        return True
    except Exception:
        return False


def _recommendations(counts: dict[str, int]) -> list[str]:
    items: list[str] = []
    if counts.get("packages", 0) == 0:
        items.append("Seed demo data or create your first package to test the workflow.")
    if counts.get("manual_analytics", 0) == 0:
        items.append("Add manual analytics entries so the insights dashboard can show useful recommendations.")
    if counts.get("prompt_templates", 0) == 0:
        items.append("Run database initialization or seed prompt templates before generating packages.")
    if not items:
        items.append("MVP is ready for daily Shorts workflow testing. Start replacing demo data with your real batches.")
    return items
