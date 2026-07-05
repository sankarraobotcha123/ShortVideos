from __future__ import annotations

from collections import defaultdict
from datetime import date, datetime
from typing import Any


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default


def _int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except Exception:
        return default


def _round(value: float, digits: int = 1) -> float:
    return round(float(value or 0), digits)


def _engagement_rate(row: dict[str, Any]) -> float:
    views = _num(row.get("views"))
    if views <= 0:
        return 0.0
    interactions = _num(row.get("likes")) + _num(row.get("comments")) + _num(row.get("shares"))
    return (interactions / views) * 100


def _parse_date(value: str | None) -> date:
    if not value:
        return date.min
    try:
        return datetime.fromisoformat(value[:10]).date()
    except Exception:
        return date.min


def _week_key(value: str | None) -> str:
    parsed = _parse_date(value)
    if parsed == date.min:
        return "Unknown week"
    year, week, _ = parsed.isocalendar()
    return f"{year}-W{week:02d}"


def _latest_rows_by_package(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest: dict[int, dict[str, Any]] = {}
    for row in rows:
        package_id = _int(row.get("package_id"))
        current = latest.get(package_id)
        if current is None:
            latest[package_id] = row
            continue
        current_key = (_parse_date(current.get("entry_date")), _int(current.get("entry_id")))
        row_key = (_parse_date(row.get("entry_date")), _int(row.get("entry_id")))
        if row_key >= current_key:
            latest[package_id] = row
    return list(latest.values())


def _public_video_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": _int(row.get("package_id")),
        "topic": row.get("topic") or "Untitled",
        "subject": row.get("subject") or "",
        "class_level": row.get("class_level") or "",
        "tone": row.get("tone") or "",
        "batch_name": row.get("batch_name") or "No batch",
        "prompt_template_name": row.get("prompt_template_name") or "No template",
        "prompt_template_style": row.get("prompt_template_style") or "",
        "review_status": row.get("review_status") or "draft",
        "trust_score": _int(row.get("trust_score")),
        "entry_date": row.get("entry_date") or "",
        "views": _int(row.get("views")),
        "likes": _int(row.get("likes")),
        "comments": _int(row.get("comments")),
        "shares": _int(row.get("shares")),
        "retention_pct": _round(_num(row.get("retention_pct"))),
        "ctr_pct": _round(_num(row.get("ctr_pct"))),
        "avg_view_duration_seconds": _round(_num(row.get("avg_view_duration_seconds"))),
        "engagement_rate_pct": _round(_engagement_rate(row), 2),
    }


def _group_performance(rows: list[dict[str, Any]], key: str, label: str, limit: int = 8) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        group_value = row.get(key) or f"No {label.lower()}"
        groups[str(group_value)].append(row)

    output: list[dict[str, Any]] = []
    for name, group_rows in groups.items():
        views = sum(_int(row.get("views")) for row in group_rows)
        interactions = sum(_int(row.get("likes")) + _int(row.get("comments")) + _int(row.get("shares")) for row in group_rows)
        avg_retention = sum(_num(row.get("retention_pct")) for row in group_rows) / max(len(group_rows), 1)
        avg_ctr = sum(_num(row.get("ctr_pct")) for row in group_rows) / max(len(group_rows), 1)
        output.append(
            {
                "name": name,
                "count": len(group_rows),
                "total_views": views,
                "avg_views": _round(views / max(len(group_rows), 1)),
                "avg_retention_pct": _round(avg_retention),
                "avg_ctr_pct": _round(avg_ctr),
                "engagement_rate_pct": _round((interactions / views * 100) if views else 0, 2),
            }
        )
    output.sort(key=lambda item: (item["total_views"], item["avg_retention_pct"]), reverse=True)
    return output[:limit]


def _weekly_summary(rows: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[_week_key(row.get("entry_date"))].append(row)
    output: list[dict[str, Any]] = []
    for week, group_rows in groups.items():
        views = sum(_int(row.get("views")) for row in group_rows)
        output.append(
            {
                "week": week,
                "entries": len(group_rows),
                "total_views": views,
                "avg_retention_pct": _round(sum(_num(row.get("retention_pct")) for row in group_rows) / max(len(group_rows), 1)),
                "avg_ctr_pct": _round(sum(_num(row.get("ctr_pct")) for row in group_rows) / max(len(group_rows), 1)),
            }
        )
    output.sort(key=lambda item: item["week"], reverse=True)
    return output[:limit]


def _recommendations(latest_rows: list[dict[str, Any]], totals: dict[str, Any], grouped: dict[str, list[dict[str, Any]]]) -> list[str]:
    if not latest_rows:
        return [
            "Enter weekly analytics for at least 5 published Shorts before making content strategy decisions.",
            "For each Short, record views, retention, likes, comments, shares, and notes about the hook or topic.",
        ]

    recommendations: list[str] = []
    top_retention = max(latest_rows, key=lambda row: _num(row.get("retention_pct")))
    top_views = max(latest_rows, key=lambda row: _int(row.get("views")))
    recommendations.append(
        f"Repeat the style of '{top_retention.get('topic')}' because it currently has the strongest retention ({_round(_num(top_retention.get('retention_pct')))}%)."
    )
    recommendations.append(
        f"Study the hook and topic framing of '{top_views.get('topic')}' because it currently has the most views ({_int(top_views.get('views'))})."
    )

    tone_groups = grouped.get("tones", [])
    if tone_groups:
        best_tone = tone_groups[0]
        recommendations.append(
            f"Use more '{best_tone['name']}' tone videos if the next batch is similar, because it leads the current tone ranking."
        )

    template_groups = grouped.get("templates", [])
    if template_groups and template_groups[0]["name"] != "No template":
        best_template = template_groups[0]
        recommendations.append(
            f"Keep testing the '{best_template['name']}' prompt template; it is currently the strongest template by views/retention balance."
        )

    avg_retention = _num(totals.get("avg_retention_pct"))
    weak = [row for row in latest_rows if _num(row.get("retention_pct")) < avg_retention and _int(row.get("views")) < _num(totals.get("avg_views_per_package"))]
    if weak:
        recommendations.append(
            f"Rewrite or re-edit {len(weak)} weak Short(s) with below-average views and retention before making many similar videos."
        )

    if len(latest_rows) < 10:
        recommendations.append("Do not over-optimize yet; collect data from at least 10–20 Shorts before finalizing your content formula.")

    return recommendations[:6]


def _report_markdown(insights: dict[str, Any]) -> str:
    totals = insights["totals"]
    lines = [
        "# Analytics Dashboard Insights",
        "",
        "## Overall snapshot",
        f"- Packages with analytics: {totals['packages_with_analytics']}",
        f"- Analytics entries: {totals['total_entries']}",
        f"- Total latest views: {totals['total_latest_views']}",
        f"- Average views per package: {totals['avg_views_per_package']}",
        f"- Average retention: {totals['avg_retention_pct']}%",
        f"- Average CTR: {totals['avg_ctr_pct']}%",
        f"- Engagement rate: {totals['engagement_rate_pct']}%",
        "",
        "## Recommendations",
    ]
    for item in insights["recommendations"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Top videos by views"])
    for item in insights["top_videos_by_views"]:
        lines.append(f"- {item['topic']} — {item['views']} views, {item['retention_pct']}% retention")

    lines.extend(["", "## Top videos by retention"])
    for item in insights["top_videos_by_retention"]:
        lines.append(f"- {item['topic']} — {item['retention_pct']}% retention, {item['views']} views")

    lines.extend(["", "## Weak videos to improve"])
    if insights["weak_videos"]:
        for item in insights["weak_videos"]:
            lines.append(f"- {item['topic']} — {item['views']} views, {item['retention_pct']}% retention")
    else:
        lines.append("- No weak videos detected yet, or not enough analytics data.")

    return "\n".join(lines) + "\n"


def build_analytics_insights(conn) -> dict[str, Any]:
    rows = [
        dict(row)
        for row in conn.execute(
            """
            SELECT
              ma.id AS entry_id,
              ma.package_id,
              ma.platform,
              ma.entry_date,
              ma.views,
              ma.likes,
              ma.comments,
              ma.shares,
              ma.avg_view_duration_seconds,
              ma.retention_pct,
              ma.ctr_pct,
              ma.notes AS analytics_notes,
              cp.topic,
              cp.subject,
              cp.class_level,
              cp.tone,
              cp.duration_seconds,
              cp.output_type,
              cp.review_status,
              cp.trust_score,
              cp.hook,
              cp.prompt_template_name,
              cp.prompt_template_style,
              b.name AS batch_name
            FROM manual_analytics ma
            JOIN content_packages cp ON cp.id = ma.package_id
            LEFT JOIN content_batches b ON b.id = cp.batch_id
            ORDER BY ma.entry_date DESC, ma.id DESC
            """
        ).fetchall()
    ]

    latest_rows = _latest_rows_by_package(rows)
    latest_public = [_public_video_row(row) for row in latest_rows]
    latest_public.sort(key=lambda item: item["views"], reverse=True)

    total_latest_views = sum(item["views"] for item in latest_public)
    total_likes = sum(item["likes"] for item in latest_public)
    total_comments = sum(item["comments"] for item in latest_public)
    total_shares = sum(item["shares"] for item in latest_public)
    avg_retention = sum(item["retention_pct"] for item in latest_public) / max(len(latest_public), 1)
    avg_ctr = sum(item["ctr_pct"] for item in latest_public) / max(len(latest_public), 1)
    avg_duration = sum(item["avg_view_duration_seconds"] for item in latest_public) / max(len(latest_public), 1)
    avg_views = total_latest_views / max(len(latest_public), 1)
    engagement_rate = ((total_likes + total_comments + total_shares) / total_latest_views * 100) if total_latest_views else 0

    totals = {
        "total_entries": len(rows),
        "packages_with_analytics": len(latest_public),
        "total_latest_views": total_latest_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "avg_views_per_package": _round(avg_views),
        "avg_retention_pct": _round(avg_retention),
        "avg_ctr_pct": _round(avg_ctr),
        "avg_view_duration_seconds": _round(avg_duration),
        "engagement_rate_pct": _round(engagement_rate, 2),
    }

    grouped = {
        "tones": _group_performance(latest_rows, "tone", "Tone"),
        "subjects": _group_performance(latest_rows, "subject", "Subject"),
        "batches": _group_performance(latest_rows, "batch_name", "Batch"),
        "templates": _group_performance(latest_rows, "prompt_template_name", "Template"),
    }

    weak_videos = [
        item
        for item in sorted(latest_public, key=lambda row: (row["retention_pct"], row["views"]))
        if item["views"] < avg_views and item["retention_pct"] < avg_retention
    ][:8]

    insights = {
        "totals": totals,
        "top_videos_by_views": latest_public[:8],
        "top_videos_by_retention": sorted(latest_public, key=lambda item: item["retention_pct"], reverse=True)[:8],
        "weak_videos": weak_videos,
        "grouped": grouped,
        "weekly_summary": _weekly_summary(rows),
        "recommendations": _recommendations(latest_rows, totals, grouped),
        "latest_entries": [_public_video_row(row) for row in rows[:12]],
        "has_enough_data": len(latest_public) >= 10,
    }
    insights["report_markdown"] = _report_markdown(insights)
    return insights
