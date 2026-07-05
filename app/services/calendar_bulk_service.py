from __future__ import annotations

from datetime import date, datetime, timedelta
import sqlite3
from typing import Any

VALID_STATUSES = {"planned", "scheduled", "published", "skipped"}
VALID_ORDER_BY = {"created_at", "trust_score", "topic"}


def _dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def _parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception as exc:
        raise ValueError("start_date must be in YYYY-MM-DD format") from exc


def _candidate_packages(conn: sqlite3.Connection, *, batch_id: int | None, limit: int, order_by: str) -> list[dict[str, Any]]:
    if limit < 1 or limit > 200:
        raise ValueError("limit must be between 1 and 200")
    if order_by not in VALID_ORDER_BY:
        order_by = "created_at"

    filters = ["pc.id NOT IN (SELECT package_id FROM publishing_calendar)"]
    params: list[Any] = []
    if batch_id is not None:
        filters.append("pc.batch_id = ?")
        params.append(batch_id)

    if order_by == "trust_score":
        order_sql = "pc.trust_score DESC, pc.id ASC"
    elif order_by == "topic":
        order_sql = "LOWER(pc.topic) ASC, pc.id ASC"
    else:
        order_sql = "pc.created_at ASC, pc.id ASC"

    params.append(limit)
    rows = conn.execute(
        f"""
        SELECT
            pc.id,
            pc.topic,
            pc.subject,
            pc.class_level,
            pc.tone,
            pc.review_status,
            pc.trust_score,
            pc.batch_id,
            cb.name AS batch_name
        FROM content_packages pc
        LEFT JOIN content_batches cb ON cb.id = pc.batch_id
        WHERE {' AND '.join(filters)}
        ORDER BY {order_sql}
        LIMIT ?
        """,
        params,
    ).fetchall()
    return [dict(row) for row in rows]


def _schedule_dates(start: date, count: int, *, videos_per_day: int, days_between: int) -> list[str]:
    videos_per_day = max(1, min(int(videos_per_day or 1), 20))
    days_between = max(0, min(int(days_between or 0), 30))
    dates: list[str] = []
    current = start
    for idx in range(count):
        if idx > 0 and idx % videos_per_day == 0:
            current = current + timedelta(days=days_between + 1)
        dates.append(current.isoformat())
    return dates


def preview_bulk_schedule(
    conn: sqlite3.Connection,
    *,
    start_date: str,
    batch_id: int | None = None,
    limit: int = 20,
    videos_per_day: int = 1,
    days_between: int = 0,
    platform: str = "YouTube Shorts",
    playlist_name: str = "",
    status: str = "planned",
    order_by: str = "created_at",
) -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")
    start = _parse_date(start_date)
    packages = _candidate_packages(conn, batch_id=batch_id, limit=limit, order_by=order_by)
    dates = _schedule_dates(start, len(packages), videos_per_day=videos_per_day, days_between=days_between)
    items = []
    for item, planned_date in zip(packages, dates):
        items.append(
            {
                **item,
                "planned_publish_date": planned_date,
                "platform": platform,
                "playlist_name": playlist_name,
                "status": status,
                "notes": f"Bulk scheduled from {item.get('batch_name') or 'unscheduled package group'}. Review final timing before publishing.",
            }
        )
    return {
        "mode": "preview",
        "batch_id": batch_id,
        "start_date": start.isoformat(),
        "limit": limit,
        "videos_per_day": videos_per_day,
        "days_between": days_between,
        "order_by": order_by,
        "platform": platform,
        "playlist_name": playlist_name,
        "status": status,
        "scheduled_count": len(items),
        "items": items,
    }


def apply_bulk_schedule(conn: sqlite3.Connection, *, created_by: str = "", **kwargs: Any) -> dict[str, Any]:
    preview = preview_bulk_schedule(conn, **kwargs)
    inserted: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for item in preview["items"]:
        try:
            cursor = conn.execute(
                """
                INSERT INTO publishing_calendar (
                    package_id, planned_publish_date, actual_publish_date, platform, status, playlist_name, notes
                ) VALUES (?, ?, '', ?, ?, ?, ?)
                """,
                (
                    int(item["id"]),
                    item["planned_publish_date"],
                    item["platform"],
                    item["status"],
                    item["playlist_name"],
                    item["notes"],
                ),
            )
            inserted.append({**item, "calendar_entry_id": int(cursor.lastrowid)})
        except sqlite3.IntegrityError:
            skipped.append({**item, "skip_reason": "Package already has a calendar entry"})

    run_payload = {
        **preview,
        "mode": "applied",
        "created_by": created_by,
        "inserted_count": len(inserted),
        "skipped_count": len(skipped),
        "inserted_items": inserted,
        "skipped_items": skipped,
    }
    conn.execute(
        """
        INSERT INTO calendar_bulk_runs (
            batch_id, start_date, limit_count, videos_per_day, days_between,
            platform, playlist_name, status, order_by, created_by,
            scheduled_count, skipped_count, run_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_payload.get("batch_id"),
            run_payload.get("start_date"),
            run_payload.get("limit"),
            run_payload.get("videos_per_day"),
            run_payload.get("days_between"),
            run_payload.get("platform"),
            run_payload.get("playlist_name"),
            run_payload.get("status"),
            run_payload.get("order_by"),
            created_by,
            len(inserted),
            len(skipped),
            __import__("json").dumps(run_payload, ensure_ascii=False, indent=2),
        ),
    )
    return run_payload


def list_bulk_runs(conn: sqlite3.Connection, limit: int = 20) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT cbr.*, cb.name AS batch_name
        FROM calendar_bulk_runs cbr
        LEFT JOIN content_batches cb ON cb.id = cbr.batch_id
        ORDER BY cbr.id DESC
        LIMIT ?
        """,
        (max(1, min(limit, 100)),),
    ).fetchall()
    return [dict(row) for row in rows]


def build_bulk_schedule_markdown(conn: sqlite3.Connection) -> str:
    runs = list_bulk_runs(conn, 50)
    lines = ["# Content Calendar Bulk Scheduling Report", ""]
    if not runs:
        lines.append("No bulk scheduling runs recorded yet.")
        return "\n".join(lines)
    for run in runs:
        lines.extend(
            [
                f"## Run #{run['id']} — {run.get('created_at', '')}",
                f"- Batch: {run.get('batch_name') or 'All unscheduled packages'}",
                f"- Start date: {run.get('start_date')}",
                f"- Platform: {run.get('platform')}",
                f"- Playlist: {run.get('playlist_name') or 'Not set'}",
                f"- Scheduled: {run.get('scheduled_count', 0)}",
                f"- Skipped: {run.get('skipped_count', 0)}",
                "",
            ]
        )
    return "\n".join(lines)
