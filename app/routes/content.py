from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.db.session import db_session
from app.services.content_generator import ContentInput
from app.services.export_service import export_package
from app.services.generation_orchestrator import generate_content_package_with_fallbacks, provider_status
from app.services.audio_service import audio_provider_status, generate_audio_asset

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# -----------------------------------------------------------------------------
# Shared helpers
# -----------------------------------------------------------------------------


def _row_to_dict(row) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _parse_json_list(value: str | None) -> list[Any]:
    try:
        parsed = json.loads(value or "[]")
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def _package_from_row(row) -> dict[str, Any]:
    package = dict(row)
    package["title_options_list"] = _parse_json_list(package.get("title_options"))
    package["hashtags_list"] = _parse_json_list(package.get("hashtags"))
    package["provider_attempts_list"] = _parse_json_list(package.get("provider_attempts"))
    package["copied_text_used"] = bool(package.get("copied_text_used"))
    return package


def _batch_from_row(row) -> dict[str, Any]:
    batch = dict(row)
    batch["planned_count"] = int(batch.get("planned_count") or 0)
    batch["completed_count"] = int(batch.get("completed_count") or 0)
    batch["published_count"] = int(batch.get("published_count") or 0)
    batch["scheduled_count"] = int(batch.get("scheduled_count") or 0)
    return batch


def _calendar_from_row(row) -> dict[str, Any]:
    item = dict(row)
    item["package_id"] = int(item.get("package_id"))
    return item


def _assert_batch_exists(conn, batch_id: int) -> None:
    existing = conn.execute("SELECT id FROM content_batches WHERE id = ?", (batch_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="Batch not found")


def _assert_package_exists(conn, package_id: int) -> None:
    existing = conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone()
    if existing is None:
        raise HTTPException(status_code=404, detail="Package not found")


def _stats(conn) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT
          COUNT(*) AS total,
          SUM(CASE WHEN review_status = 'approved' THEN 1 ELSE 0 END) AS approved,
          SUM(CASE WHEN review_status = 'draft' THEN 1 ELSE 0 END) AS draft,
          SUM(CASE WHEN review_status = 'published' THEN 1 ELSE 0 END) AS published,
          AVG(trust_score) AS avg_trust
        FROM content_packages
        """
    ).fetchone()
    data = dict(row or {})
    for key in ["total", "approved", "draft", "published"]:
        data[key] = int(data.get(key) or 0)
    data["avg_trust"] = round(float(data.get("avg_trust") or 0), 1)

    batch_row = conn.execute(
        """
        SELECT
          COUNT(*) AS total_batches,
          SUM(CASE WHEN status IN ('planning', 'active') THEN 1 ELSE 0 END) AS active_batches
        FROM content_batches
        """
    ).fetchone()
    calendar_row = conn.execute(
        """
        SELECT
          COUNT(*) AS scheduled_items,
          SUM(CASE WHEN status = 'published' THEN 1 ELSE 0 END) AS calendar_published
        FROM publishing_calendar
        """
    ).fetchone()
    batch_data = dict(batch_row or {})
    calendar_data = dict(calendar_row or {})
    data.update({key: int(batch_data.get(key) or 0) for key in ["total_batches", "active_batches"]})
    data.update({key: int(calendar_data.get(key) or 0) for key in ["scheduled_items", "calendar_published"]})
    return data


def _insert_generated_package(inp: ContentInput, generated: dict[str, Any], batch_id: int | None = None) -> int:
    with db_session() as conn:
        cursor = conn.execute(
            """
            INSERT INTO content_packages (
                board_source, class_level, subject, topic, audience, language, duration_seconds,
                output_type, tone, source_notes, source_name, source_license_type,
                page_or_section_reference, copied_text_used, transformation_notes,
                hook, script_text, storyboard_markdown, subtitle_srt, visual_prompts_markdown,
                title_options, description, hashtags, quiz_question, trust_score,
                provider_used, generation_mode, provider_chain, provider_notes, provider_attempts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
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
                generated["trust_score"],
                generated.get("provider_used", "template"),
                generated.get("generation_mode", "deterministic_template"),
                generated.get("provider_chain", "template"),
                generated.get("provider_notes", ""),
                generated.get("provider_attempts", "[]"),
            ),
        )
        package_id = int(cursor.lastrowid)
        if batch_id is not None:
            _assert_batch_exists(conn, batch_id)
            conn.execute("UPDATE content_packages SET batch_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (batch_id, package_id))
        return package_id


def _content_input_from_form(
    board_source: str,
    class_level: str,
    subject: str,
    topic: str,
    audience: str,
    language: str,
    duration_seconds: int,
    output_type: str,
    tone: str,
    source_notes: str,
    source_name: str,
    source_license_type: str,
    page_or_section_reference: str,
    copied_text_used: str,
    transformation_notes: str,
) -> ContentInput:
    copied = copied_text_used in {"on", "true", "1", "yes"}
    return ContentInput(
        board_source=board_source,
        class_level=class_level,
        subject=subject,
        topic=topic,
        audience=audience,
        language=language,
        duration_seconds=duration_seconds,
        output_type=output_type,
        tone=tone,
        source_notes=source_notes,
        source_name=source_name,
        source_license_type=source_license_type,
        page_or_section_reference=page_or_section_reference,
        copied_text_used=copied,
        transformation_notes=transformation_notes,
    )


# -----------------------------------------------------------------------------
# Legacy Jinja UI. Kept as a fallback while React/npm becomes the main UI.
# -----------------------------------------------------------------------------


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    with db_session() as conn:
        packages = conn.execute(
            "SELECT id, topic, subject, class_level, trust_score, review_status, created_at FROM content_packages ORDER BY id DESC"
        ).fetchall()
        stats = _stats(conn)
    return templates.TemplateResponse("index.html", {"request": request, "packages": packages, "stats": stats})


@router.get("/content/new", response_class=HTMLResponse)
def new_content_form(request: Request):
    return templates.TemplateResponse("new_content.html", {"request": request})


@router.get("/settings/ai", response_class=HTMLResponse)
def ai_provider_settings(request: Request):
    return templates.TemplateResponse(
        "provider_status.html",
        {"request": request, "providers": provider_status()},
    )


@router.post("/content/generate")
def generate_content(
    board_source: str = Form(...),
    class_level: str = Form(...),
    subject: str = Form(...),
    topic: str = Form(...),
    audience: str = Form(...),
    language: str = Form("English"),
    duration_seconds: int = Form(60),
    output_type: str = Form("Short"),
    tone: str = Form("Curious"),
    source_notes: str = Form(""),
    source_name: str = Form(""),
    source_license_type: str = Form(""),
    page_or_section_reference: str = Form(""),
    copied_text_used: str = Form("off"),
    transformation_notes: str = Form(""),
):
    inp = _content_input_from_form(
        board_source,
        class_level,
        subject,
        topic,
        audience,
        language,
        duration_seconds,
        output_type,
        tone,
        source_notes,
        source_name,
        source_license_type,
        page_or_section_reference,
        copied_text_used,
        transformation_notes,
    )
    generated = generate_content_package_with_fallbacks(inp)
    package_id = _insert_generated_package(inp, generated)
    return RedirectResponse(f"/content/{package_id}", status_code=303)


@router.get("/content/{package_id}", response_class=HTMLResponse)
def package_detail(request: Request, package_id: int):
    with db_session() as conn:
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        analytics = conn.execute(
            "SELECT * FROM manual_analytics WHERE package_id = ? ORDER BY entry_date DESC, id DESC",
            (package_id,),
        ).fetchall()
    if row is None:
        raise HTTPException(status_code=404, detail="Package not found")
    package = _package_from_row(row)
    return templates.TemplateResponse(
        "package_detail.html",
        {"request": request, "package": package, "analytics": analytics},
    )


@router.post("/content/{package_id}/review")
def update_review(
    package_id: int,
    review_status: str = Form(...),
    script_text: str = Form(...),
    reviewer_notes: str = Form(""),
):
    _update_review_record(package_id, review_status, script_text, reviewer_notes)
    return RedirectResponse(f"/content/{package_id}", status_code=303)


@router.post("/content/{package_id}/analytics")
def add_analytics(
    package_id: int,
    platform: str = Form("YouTube Shorts"),
    entry_date: str = Form(...),
    views: int = Form(0),
    likes: int = Form(0),
    comments: int = Form(0),
    shares: int = Form(0),
    avg_view_duration_seconds: float = Form(0),
    retention_pct: float = Form(0),
    ctr_pct: float = Form(0),
    notes: str = Form(""),
):
    _insert_analytics_record(
        package_id,
        platform,
        entry_date,
        views,
        likes,
        comments,
        shares,
        avg_view_duration_seconds,
        retention_pct,
        ctr_pct,
        notes,
    )
    return RedirectResponse(f"/content/{package_id}", status_code=303)


@router.get("/content/{package_id}/export")
def export_content(package_id: int):
    with db_session() as conn:
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        audio_assets = conn.execute("SELECT * FROM audio_assets WHERE package_id = ? ORDER BY id DESC", (package_id,)).fetchall()
    if row is None:
        raise HTTPException(status_code=404, detail="Package not found")
    zip_path = export_package(dict(row), [dict(item) for item in audio_assets])
    return FileResponse(zip_path, filename=Path(zip_path).name, media_type="application/zip")


# -----------------------------------------------------------------------------
# React/npm frontend API.
# -----------------------------------------------------------------------------


class ContentGenerateRequest(BaseModel):
    board_source: str = Field(..., min_length=1)
    class_level: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1)
    topic: str = Field(..., min_length=1)
    audience: str = Field(..., min_length=1)
    language: str = "English"
    duration_seconds: int = Field(60, ge=20, le=90)
    output_type: str = "Short"
    tone: str = "Curious"
    source_notes: str = ""
    source_name: str = ""
    source_license_type: str = ""
    page_or_section_reference: str = ""
    copied_text_used: bool = False
    transformation_notes: str = ""
    batch_id: int | None = None

    def to_content_input(self) -> ContentInput:
        data = self.model_dump(exclude={"batch_id"})
        return ContentInput(**data)


class ReviewUpdateRequest(BaseModel):
    review_status: str
    script_text: str
    reviewer_notes: str = ""


class AnalyticsCreateRequest(BaseModel):
    platform: str = "YouTube Shorts"
    entry_date: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    avg_view_duration_seconds: float = 0
    retention_pct: float = 0
    ctr_pct: float = 0
    notes: str = ""


class BatchCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    niche: str = "Class 6-8 Science curiosity Shorts"
    target_audience: str = "School students and curious learners"
    start_date: str = ""
    end_date: str = ""
    planned_count: int = Field(20, ge=1, le=200)
    status: str = "planning"
    notes: str = ""


class BatchUpdateRequest(BaseModel):
    name: str
    niche: str = ""
    target_audience: str = ""
    start_date: str = ""
    end_date: str = ""
    planned_count: int = Field(20, ge=1, le=200)
    status: str = "planning"
    notes: str = ""


class PackageBatchUpdateRequest(BaseModel):
    batch_id: int | None = None


class CalendarCreateRequest(BaseModel):
    package_id: int
    planned_publish_date: str
    actual_publish_date: str = ""
    platform: str = "YouTube Shorts"
    status: str = "planned"
    playlist_name: str = ""
    notes: str = ""


class CalendarUpdateRequest(BaseModel):
    planned_publish_date: str
    actual_publish_date: str = ""
    platform: str = "YouTube Shorts"
    status: str = "planned"
    playlist_name: str = ""
    notes: str = ""


@router.get("/api/packages")
def api_packages() -> dict[str, Any]:
    with db_session() as conn:
        rows = conn.execute(
            """
            SELECT cp.id, cp.batch_id, cp.topic, cp.subject, cp.class_level, cp.language, cp.duration_seconds,
                   cp.trust_score, cp.review_status, cp.provider_used, cp.created_at, b.name AS batch_name
            FROM content_packages cp
            LEFT JOIN content_batches b ON b.id = cp.batch_id
            ORDER BY cp.id DESC
            """
        ).fetchall()
        stats = _stats(conn)
    return {"stats": stats, "packages": [dict(row) for row in rows]}


@router.post("/api/content/generate", status_code=201)
def api_generate_content(payload: ContentGenerateRequest) -> dict[str, Any]:
    inp = payload.to_content_input()
    generated = generate_content_package_with_fallbacks(inp)
    package_id = _insert_generated_package(inp, generated, payload.batch_id)
    with db_session() as conn:
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
    return {"package": _package_from_row(row)}


@router.get("/api/content/{package_id}")
def api_package(package_id: int) -> dict[str, Any]:
    with db_session() as conn:
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        analytics = conn.execute(
            "SELECT * FROM manual_analytics WHERE package_id = ? ORDER BY entry_date DESC, id DESC",
            (package_id,),
        ).fetchall()
        calendar = conn.execute(
            "SELECT * FROM publishing_calendar WHERE package_id = ?",
            (package_id,),
        ).fetchone()
        audio_assets = conn.execute(
            "SELECT * FROM audio_assets WHERE package_id = ? ORDER BY id DESC",
            (package_id,),
        ).fetchall()
    if row is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return {
        "package": _package_from_row(row),
        "analytics": [dict(item) for item in analytics],
        "calendar": dict(calendar) if calendar else None,
        "audio_assets": [dict(item) for item in audio_assets],
    }


@router.patch("/api/content/{package_id}/review")
def api_update_review(package_id: int, payload: ReviewUpdateRequest) -> dict[str, Any]:
    _update_review_record(package_id, payload.review_status, payload.script_text, payload.reviewer_notes)
    with db_session() as conn:
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
    return {"package": _package_from_row(row)}


@router.post("/api/content/{package_id}/analytics", status_code=201)
def api_add_analytics(package_id: int, payload: AnalyticsCreateRequest) -> dict[str, Any]:
    _insert_analytics_record(
        package_id,
        payload.platform,
        payload.entry_date,
        payload.views,
        payload.likes,
        payload.comments,
        payload.shares,
        payload.avg_view_duration_seconds,
        payload.retention_pct,
        payload.ctr_pct,
        payload.notes,
    )
    with db_session() as conn:
        rows = conn.execute(
            "SELECT * FROM manual_analytics WHERE package_id = ? ORDER BY entry_date DESC, id DESC",
            (package_id,),
        ).fetchall()
    return {"analytics": [dict(row) for row in rows]}


@router.get("/api/batches")
def api_batches() -> dict[str, Any]:
    with db_session() as conn:
        rows = conn.execute(
            """
            SELECT
              b.*,
              COUNT(cp.id) AS completed_count,
              SUM(CASE WHEN cp.review_status = 'published' THEN 1 ELSE 0 END) AS published_count,
              COUNT(pc.id) AS scheduled_count
            FROM content_batches b
            LEFT JOIN content_packages cp ON cp.batch_id = b.id
            LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
            GROUP BY b.id
            ORDER BY b.created_at DESC, b.id DESC
            """
        ).fetchall()
        unassigned = conn.execute(
            """
            SELECT id, topic, subject, class_level, review_status, trust_score, created_at
            FROM content_packages
            WHERE batch_id IS NULL
            ORDER BY id DESC
            """
        ).fetchall()
    return {"batches": [_batch_from_row(row) for row in rows], "unassigned_packages": [dict(row) for row in unassigned]}


@router.post("/api/batches", status_code=201)
def api_create_batch(payload: BatchCreateRequest) -> dict[str, Any]:
    _validate_batch_status(payload.status)
    with db_session() as conn:
        cursor = conn.execute(
            """
            INSERT INTO content_batches (name, niche, target_audience, start_date, end_date, planned_count, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.name,
                payload.niche,
                payload.target_audience,
                payload.start_date,
                payload.end_date,
                payload.planned_count,
                payload.status,
                payload.notes,
            ),
        )
        batch_id = int(cursor.lastrowid)
        row = conn.execute(
            """
            SELECT b.*, 0 AS completed_count, 0 AS published_count, 0 AS scheduled_count
            FROM content_batches b WHERE b.id = ?
            """,
            (batch_id,),
        ).fetchone()
    return {"batch": _batch_from_row(row)}


@router.get("/api/batches/{batch_id}")
def api_batch_detail(batch_id: int) -> dict[str, Any]:
    with db_session() as conn:
        row = conn.execute(
            """
            SELECT
              b.*,
              COUNT(cp.id) AS completed_count,
              SUM(CASE WHEN cp.review_status = 'published' THEN 1 ELSE 0 END) AS published_count,
              COUNT(pc.id) AS scheduled_count
            FROM content_batches b
            LEFT JOIN content_packages cp ON cp.batch_id = b.id
            LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
            WHERE b.id = ?
            GROUP BY b.id
            """,
            (batch_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Batch not found")
        packages = conn.execute(
            """
            SELECT cp.id, cp.topic, cp.subject, cp.class_level, cp.language, cp.duration_seconds,
                   cp.trust_score, cp.review_status, cp.created_at,
                   pc.planned_publish_date, pc.status AS calendar_status, pc.platform
            FROM content_packages cp
            LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
            WHERE cp.batch_id = ?
            ORDER BY cp.id DESC
            """,
            (batch_id,),
        ).fetchall()
    return {"batch": _batch_from_row(row), "packages": [dict(item) for item in packages]}


@router.patch("/api/batches/{batch_id}")
def api_update_batch(batch_id: int, payload: BatchUpdateRequest) -> dict[str, Any]:
    _validate_batch_status(payload.status)
    with db_session() as conn:
        _assert_batch_exists(conn, batch_id)
        conn.execute(
            """
            UPDATE content_batches
            SET name = ?, niche = ?, target_audience = ?, start_date = ?, end_date = ?,
                planned_count = ?, status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                payload.name,
                payload.niche,
                payload.target_audience,
                payload.start_date,
                payload.end_date,
                payload.planned_count,
                payload.status,
                payload.notes,
                batch_id,
            ),
        )
        row = conn.execute(
            """
            SELECT b.*,
                   COUNT(cp.id) AS completed_count,
                   SUM(CASE WHEN cp.review_status = 'published' THEN 1 ELSE 0 END) AS published_count,
                   COUNT(pc.id) AS scheduled_count
            FROM content_batches b
            LEFT JOIN content_packages cp ON cp.batch_id = b.id
            LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
            WHERE b.id = ?
            GROUP BY b.id
            """,
            (batch_id,),
        ).fetchone()
    return {"batch": _batch_from_row(row)}


@router.patch("/api/content/{package_id}/batch")
def api_assign_package_batch(package_id: int, payload: PackageBatchUpdateRequest) -> dict[str, Any]:
    with db_session() as conn:
        _assert_package_exists(conn, package_id)
        if payload.batch_id is not None:
            _assert_batch_exists(conn, payload.batch_id)
        conn.execute(
            "UPDATE content_packages SET batch_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (payload.batch_id, package_id),
        )
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
    return {"package": _package_from_row(row)}


@router.get("/api/calendar")
def api_calendar() -> dict[str, Any]:
    with db_session() as conn:
        entries = conn.execute(
            """
            SELECT pc.*, cp.topic, cp.subject, cp.class_level, cp.review_status, cp.trust_score, cp.batch_id, b.name AS batch_name
            FROM publishing_calendar pc
            JOIN content_packages cp ON cp.id = pc.package_id
            LEFT JOIN content_batches b ON b.id = cp.batch_id
            ORDER BY pc.planned_publish_date ASC, pc.id ASC
            """
        ).fetchall()
        unscheduled = conn.execute(
            """
            SELECT cp.id, cp.topic, cp.subject, cp.class_level, cp.review_status, cp.trust_score, cp.batch_id, b.name AS batch_name
            FROM content_packages cp
            LEFT JOIN content_batches b ON b.id = cp.batch_id
            LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
            WHERE pc.id IS NULL
            ORDER BY cp.id DESC
            """
        ).fetchall()
    return {"calendar": [_calendar_from_row(row) for row in entries], "unscheduled_packages": [dict(row) for row in unscheduled]}


@router.post("/api/calendar", status_code=201)
def api_create_calendar_entry(payload: CalendarCreateRequest) -> dict[str, Any]:
    _validate_calendar_status(payload.status)
    with db_session() as conn:
        _assert_package_exists(conn, payload.package_id)
        conn.execute(
            """
            INSERT INTO publishing_calendar (
                package_id, planned_publish_date, actual_publish_date, platform, status, playlist_name, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(package_id) DO UPDATE SET
                planned_publish_date = excluded.planned_publish_date,
                actual_publish_date = excluded.actual_publish_date,
                platform = excluded.platform,
                status = excluded.status,
                playlist_name = excluded.playlist_name,
                notes = excluded.notes,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                payload.package_id,
                payload.planned_publish_date,
                payload.actual_publish_date,
                payload.platform,
                payload.status,
                payload.playlist_name,
                payload.notes,
            ),
        )
        row = conn.execute(
            """
            SELECT pc.*, cp.topic, cp.subject, cp.class_level, cp.review_status, cp.trust_score, cp.batch_id, b.name AS batch_name
            FROM publishing_calendar pc
            JOIN content_packages cp ON cp.id = pc.package_id
            LEFT JOIN content_batches b ON b.id = cp.batch_id
            WHERE pc.package_id = ?
            """,
            (payload.package_id,),
        ).fetchone()
    return {"calendar_entry": _calendar_from_row(row)}


@router.patch("/api/calendar/{entry_id}")
def api_update_calendar_entry(entry_id: int, payload: CalendarUpdateRequest) -> dict[str, Any]:
    _validate_calendar_status(payload.status)
    with db_session() as conn:
        existing = conn.execute("SELECT id FROM publishing_calendar WHERE id = ?", (entry_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Calendar entry not found")
        conn.execute(
            """
            UPDATE publishing_calendar
            SET planned_publish_date = ?, actual_publish_date = ?, platform = ?, status = ?,
                playlist_name = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                payload.planned_publish_date,
                payload.actual_publish_date,
                payload.platform,
                payload.status,
                payload.playlist_name,
                payload.notes,
                entry_id,
            ),
        )
        row = conn.execute(
            """
            SELECT pc.*, cp.topic, cp.subject, cp.class_level, cp.review_status, cp.trust_score, cp.batch_id, b.name AS batch_name
            FROM publishing_calendar pc
            JOIN content_packages cp ON cp.id = pc.package_id
            LEFT JOIN content_batches b ON b.id = cp.batch_id
            WHERE pc.id = ?
            """,
            (entry_id,),
        ).fetchone()
    return {"calendar_entry": _calendar_from_row(row)}


@router.delete("/api/calendar/{entry_id}")
def api_delete_calendar_entry(entry_id: int) -> dict[str, Any]:
    with db_session() as conn:
        existing = conn.execute("SELECT id FROM publishing_calendar WHERE id = ?", (entry_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Calendar entry not found")
        conn.execute("DELETE FROM publishing_calendar WHERE id = ?", (entry_id,))
    return {"deleted": True, "entry_id": entry_id}


@router.post("/api/content/{package_id}/audio", status_code=201)
def api_generate_audio(package_id: int) -> dict[str, Any]:
    with db_session() as conn:
        row = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Package not found")
        payload = generate_audio_asset(dict(row))
        cursor = conn.execute(
            """
            INSERT INTO audio_assets (
                package_id, provider_used, status, file_path, file_name, mime_type, voice_id,
                duration_seconds, script_snapshot, provider_notes, provider_attempts
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                package_id,
                payload["provider_used"],
                payload["status"],
                payload["file_path"],
                payload["file_name"],
                payload["mime_type"],
                payload.get("voice_id", ""),
                payload.get("duration_seconds", 0),
                payload["script_snapshot"],
                payload.get("provider_notes", ""),
                payload.get("provider_attempts", "[]"),
            ),
        )
        asset_id = int(cursor.lastrowid)
        asset = conn.execute("SELECT * FROM audio_assets WHERE id = ?", (asset_id,)).fetchone()
    return {"audio_asset": dict(asset)}


@router.get("/api/content/{package_id}/audio")
def api_list_audio(package_id: int) -> dict[str, Any]:
    with db_session() as conn:
        _assert_package_exists(conn, package_id)
        rows = conn.execute("SELECT * FROM audio_assets WHERE package_id = ? ORDER BY id DESC", (package_id,)).fetchall()
    return {"audio_assets": [dict(row) for row in rows]}


@router.get("/content/{package_id}/audio/{asset_id}/download")
def download_audio_asset(package_id: int, asset_id: int):
    with db_session() as conn:
        row = conn.execute(
            "SELECT * FROM audio_assets WHERE id = ? AND package_id = ?",
            (asset_id, package_id),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Audio asset not found")
    path = Path(row["file_path"])
    if not path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found on disk")
    return FileResponse(path, filename=row["file_name"], media_type=row["mime_type"] or "application/octet-stream")


@router.get("/api/settings/audio")
def api_audio_settings() -> dict[str, Any]:
    return {"providers": audio_provider_status()}


@router.get("/api/settings/ai")
def api_ai_settings() -> dict[str, Any]:
    return {"providers": provider_status()}


# -----------------------------------------------------------------------------
# Record mutators used by both Jinja forms and React API.
# -----------------------------------------------------------------------------


def _validate_batch_status(status: str) -> None:
    allowed = {"planning", "active", "completed", "paused"}
    if status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid batch status")


def _validate_calendar_status(status: str) -> None:
    allowed = {"planned", "scheduled", "published", "skipped"}
    if status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid calendar status")


def _update_review_record(package_id: int, review_status: str, script_text: str, reviewer_notes: str) -> None:
    allowed = {"draft", "approved", "edit_required", "rejected", "published"}
    if review_status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid review status")
    with db_session() as conn:
        existing = conn.execute("SELECT * FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Package not found")
        conn.execute(
            """
            UPDATE content_packages
            SET review_status = ?, script_text = ?, reviewer_notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (review_status, script_text, reviewer_notes, package_id),
        )


def _insert_analytics_record(
    package_id: int,
    platform: str,
    entry_date: str,
    views: int,
    likes: int,
    comments: int,
    shares: int,
    avg_view_duration_seconds: float,
    retention_pct: float,
    ctr_pct: float,
    notes: str,
) -> None:
    with db_session() as conn:
        existing = conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Package not found")
        conn.execute(
            """
            INSERT INTO manual_analytics (
                package_id, platform, entry_date, views, likes, comments, shares,
                avg_view_duration_seconds, retention_pct, ctr_pct, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                package_id,
                platform,
                entry_date,
                views,
                likes,
                comments,
                shares,
                avg_view_duration_seconds,
                retention_pct,
                ctr_pct,
                notes,
            ),
        )
