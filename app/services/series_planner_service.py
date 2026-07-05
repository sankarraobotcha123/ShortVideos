from __future__ import annotations

from typing import Any

SERIES_STATUSES = ["planning", "active", "completed", "paused", "archived"]
EPISODE_STATUSES = ["planned", "idea_ready", "package_created", "scheduled", "published", "skipped"]


def _clean(value: Any, default: str = "") -> str:
    return str(value if value is not None else default).strip()


def serialize_series(row: Any) -> dict[str, Any]:
    series = dict(row)
    series["planned_count"] = int(series.get("planned_count") or 0)
    for key in ["episode_count", "package_count", "idea_count", "published_count", "scheduled_count"]:
        series[key] = int(series.get(key) or 0)
    return series


def serialize_series_item(row: Any) -> dict[str, Any]:
    item = dict(row)
    item["order_index"] = int(item.get("order_index") or 0)
    item["series_id"] = int(item.get("series_id") or 0)
    item["idea_id"] = item.get("idea_id") or None
    item["package_id"] = item.get("package_id") or None
    return item


def list_content_series(conn) -> dict[str, Any]:
    rows = conn.execute(
        """
        SELECT
          cs.*,
          COUNT(csi.id) AS episode_count,
          SUM(CASE WHEN csi.package_id IS NOT NULL THEN 1 ELSE 0 END) AS package_count,
          SUM(CASE WHEN csi.idea_id IS NOT NULL THEN 1 ELSE 0 END) AS idea_count,
          SUM(CASE WHEN pc.status = 'published' OR cp.review_status = 'published' THEN 1 ELSE 0 END) AS published_count,
          SUM(CASE WHEN pc.status IN ('planned', 'scheduled') THEN 1 ELSE 0 END) AS scheduled_count
        FROM content_series cs
        LEFT JOIN content_series_items csi ON csi.series_id = cs.id
        LEFT JOIN content_packages cp ON cp.id = csi.package_id
        LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
        GROUP BY cs.id
        ORDER BY
          CASE cs.status
            WHEN 'active' THEN 1
            WHEN 'planning' THEN 2
            WHEN 'paused' THEN 3
            WHEN 'completed' THEN 4
            ELSE 5
          END,
          cs.updated_at DESC,
          cs.id DESC
        """
    ).fetchall()
    series = [serialize_series(row) for row in rows]
    return {"series": series, "summary": summarize_series(series)}


def summarize_series(series: list[dict[str, Any]]) -> dict[str, Any]:
    by_status = {status: 0 for status in SERIES_STATUSES}
    total_episodes = 0
    total_published = 0
    for item in series:
        by_status[str(item.get("status") or "planning")] = by_status.get(str(item.get("status") or "planning"), 0) + 1
        total_episodes += int(item.get("episode_count") or 0)
        total_published += int(item.get("published_count") or 0)
    return {
        "total_series": len(series),
        "by_status": by_status,
        "total_episodes": total_episodes,
        "total_published": total_published,
        "active_or_planning": by_status.get("active", 0) + by_status.get("planning", 0),
    }


def get_content_series(conn, series_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT
          cs.*,
          COUNT(csi.id) AS episode_count,
          SUM(CASE WHEN csi.package_id IS NOT NULL THEN 1 ELSE 0 END) AS package_count,
          SUM(CASE WHEN csi.idea_id IS NOT NULL THEN 1 ELSE 0 END) AS idea_count,
          SUM(CASE WHEN pc.status = 'published' OR cp.review_status = 'published' THEN 1 ELSE 0 END) AS published_count,
          SUM(CASE WHEN pc.status IN ('planned', 'scheduled') THEN 1 ELSE 0 END) AS scheduled_count
        FROM content_series cs
        LEFT JOIN content_series_items csi ON csi.series_id = cs.id
        LEFT JOIN content_packages cp ON cp.id = csi.package_id
        LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
        WHERE cs.id = ?
        GROUP BY cs.id
        """,
        (series_id,),
    ).fetchone()
    return serialize_series(row) if row else None


def list_series_items(conn, series_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT
          csi.*,
          ci.title AS idea_title,
          ci.status AS idea_status,
          ci.total_score AS idea_score,
          ci.priority AS idea_priority,
          cp.topic AS package_topic,
          cp.review_status AS package_review_status,
          cp.trust_score AS package_trust_score,
          pc.planned_publish_date,
          pc.status AS calendar_status
        FROM content_series_items csi
        LEFT JOIN content_ideas ci ON ci.id = csi.idea_id
        LEFT JOIN content_packages cp ON cp.id = csi.package_id
        LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
        WHERE csi.series_id = ?
        ORDER BY csi.order_index ASC, csi.id ASC
        """,
        (series_id,),
    ).fetchall()
    return [serialize_series_item(row) for row in rows]


def create_content_series(conn, payload: dict[str, Any]) -> dict[str, Any]:
    status = _clean(payload.get("status"), "planning") or "planning"
    if status not in SERIES_STATUSES:
        raise ValueError("Invalid series status")
    cursor = conn.execute(
        """
        INSERT INTO content_series (
            title, niche, target_audience, subject, class_level, language, series_goal,
            status, planned_count, episode_style, cta_strategy, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            _clean(payload.get("title")),
            _clean(payload.get("niche"), "Class 6-8 Science curiosity Shorts"),
            _clean(payload.get("target_audience"), "School students and curious learners"),
            _clean(payload.get("subject"), "Science"),
            _clean(payload.get("class_level"), "Class 7"),
            _clean(payload.get("language"), "English"),
            _clean(payload.get("series_goal"), "Build curiosity and bring viewers to the next Short."),
            status,
            int(payload.get("planned_count") or 10),
            _clean(payload.get("episode_style"), "Curiosity → explanation → challenge"),
            _clean(payload.get("cta_strategy"), "End with a reason to watch the next episode."),
            _clean(payload.get("notes")),
        ),
    )
    return get_content_series(conn, int(cursor.lastrowid)) or {}


def update_content_series(conn, series_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    existing = get_content_series(conn, series_id)
    if existing is None:
        raise ValueError("Content series not found")
    merged = {**existing, **payload}
    status = _clean(merged.get("status"), "planning") or "planning"
    if status not in SERIES_STATUSES:
        raise ValueError("Invalid series status")
    conn.execute(
        """
        UPDATE content_series
        SET title = ?, niche = ?, target_audience = ?, subject = ?, class_level = ?, language = ?,
            series_goal = ?, status = ?, planned_count = ?, episode_style = ?, cta_strategy = ?, notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (
            _clean(merged.get("title")),
            _clean(merged.get("niche")),
            _clean(merged.get("target_audience")),
            _clean(merged.get("subject"), "Science"),
            _clean(merged.get("class_level"), "Class 7"),
            _clean(merged.get("language"), "English"),
            _clean(merged.get("series_goal")),
            status,
            int(merged.get("planned_count") or 10),
            _clean(merged.get("episode_style")),
            _clean(merged.get("cta_strategy")),
            _clean(merged.get("notes")),
            series_id,
        ),
    )
    return get_content_series(conn, series_id) or {}


def create_series_item(conn, series_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    if get_content_series(conn, series_id) is None:
        raise ValueError("Content series not found")
    status = _clean(payload.get("target_status"), "planned") or "planned"
    if status not in EPISODE_STATUSES:
        raise ValueError("Invalid episode status")
    idea_id = payload.get("idea_id") or None
    package_id = payload.get("package_id") or None
    if idea_id and conn.execute("SELECT id FROM content_ideas WHERE id = ?", (idea_id,)).fetchone() is None:
        raise ValueError("Linked idea not found")
    if package_id and conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone() is None:
        raise ValueError("Linked package not found")
    cursor = conn.execute(
        """
        INSERT INTO content_series_items (
            series_id, idea_id, package_id, order_index, episode_title, hook_angle, target_status, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            series_id,
            idea_id,
            package_id,
            int(payload.get("order_index") or 1),
            _clean(payload.get("episode_title")),
            _clean(payload.get("hook_angle")),
            status,
            _clean(payload.get("notes")),
        ),
    )
    return get_series_item(conn, int(cursor.lastrowid)) or {}


def get_series_item(conn, item_id: int) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT csi.*, ci.title AS idea_title, ci.status AS idea_status, ci.total_score AS idea_score,
               ci.priority AS idea_priority, cp.topic AS package_topic, cp.review_status AS package_review_status,
               cp.trust_score AS package_trust_score, pc.planned_publish_date, pc.status AS calendar_status
        FROM content_series_items csi
        LEFT JOIN content_ideas ci ON ci.id = csi.idea_id
        LEFT JOIN content_packages cp ON cp.id = csi.package_id
        LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
        WHERE csi.id = ?
        """,
        (item_id,),
    ).fetchone()
    return serialize_series_item(row) if row else None


def update_series_item(conn, series_id: int, item_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    existing = get_series_item(conn, item_id)
    if existing is None or int(existing["series_id"]) != series_id:
        raise ValueError("Series item not found")
    merged = {**existing, **payload}
    status = _clean(merged.get("target_status"), "planned") or "planned"
    if status not in EPISODE_STATUSES:
        raise ValueError("Invalid episode status")
    idea_id = merged.get("idea_id") or None
    package_id = merged.get("package_id") or None
    if idea_id and conn.execute("SELECT id FROM content_ideas WHERE id = ?", (idea_id,)).fetchone() is None:
        raise ValueError("Linked idea not found")
    if package_id and conn.execute("SELECT id FROM content_packages WHERE id = ?", (package_id,)).fetchone() is None:
        raise ValueError("Linked package not found")
    conn.execute(
        """
        UPDATE content_series_items
        SET idea_id = ?, package_id = ?, order_index = ?, episode_title = ?, hook_angle = ?,
            target_status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ? AND series_id = ?
        """,
        (
            idea_id,
            package_id,
            int(merged.get("order_index") or 1),
            _clean(merged.get("episode_title")),
            _clean(merged.get("hook_angle")),
            status,
            _clean(merged.get("notes")),
            item_id,
            series_id,
        ),
    )
    return get_series_item(conn, item_id) or {}


def build_content_series_markdown(series_payload: dict[str, Any]) -> str:
    series_list = series_payload.get("series", [])
    summary = series_payload.get("summary", {})
    lines = [
        "# Content Series Planner",
        "",
        f"Total series: {summary.get('total_series', 0)}",
        f"Total episodes: {summary.get('total_episodes', 0)}",
        f"Published episodes: {summary.get('total_published', 0)}",
        "",
    ]
    for series in series_list:
        lines.extend(
            [
                f"## #{series.get('id')} - {series.get('title')}",
                f"- Status: {series.get('status')}",
                f"- Subject/Level: {series.get('subject')} / {series.get('class_level')}",
                f"- Goal: {series.get('series_goal') or '-'}",
                f"- Planned episodes: {series.get('planned_count')}",
                f"- Current episodes: {series.get('episode_count')}",
                f"- CTA strategy: {series.get('cta_strategy') or '-'}",
                "",
            ]
        )
    return "\n".join(lines)


def build_single_series_markdown(series: dict[str, Any], items: list[dict[str, Any]]) -> str:
    lines = [
        f"# Series Plan: {series.get('title')}",
        "",
        f"Status: {series.get('status')}",
        f"Niche: {series.get('niche')}",
        f"Audience: {series.get('target_audience')}",
        f"Subject/Level: {series.get('subject')} / {series.get('class_level')}",
        f"Series goal: {series.get('series_goal')}",
        f"Episode style: {series.get('episode_style')}",
        f"CTA strategy: {series.get('cta_strategy')}",
        "",
        "## Episodes",
        "",
    ]
    for item in items:
        linked = item.get("package_topic") or item.get("idea_title") or "Not linked yet"
        lines.extend(
            [
                f"### Episode {item.get('order_index')}: {item.get('episode_title') or linked}",
                f"- Status: {item.get('target_status')}",
                f"- Hook: {item.get('hook_angle') or '-'}",
                f"- Linked: {linked}",
                f"- Notes: {item.get('notes') or '-'}",
                "",
            ]
        )
    return "\n".join(lines)
