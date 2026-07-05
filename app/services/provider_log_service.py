from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, Iterable


def parse_provider_attempts(raw_attempts: str | None) -> list[dict[str, Any]]:
    try:
        attempts = json.loads(raw_attempts or "[]")
        if not isinstance(attempts, list):
            return []
        return [item for item in attempts if isinstance(item, dict)]
    except Exception:
        return []


def record_generation_provider_logs(conn, package_id: int, generated: dict[str, Any]) -> int:
    """Persist provider attempts for a generated package.

    The content package already stores provider_attempts as JSON. This table is
    a query-friendly audit log so the UI can show fallback reliability over time.
    """

    attempts = parse_provider_attempts(generated.get("provider_attempts"))
    if not attempts:
        attempts = [
            {
                "provider": generated.get("provider_used", "template"),
                "available": True,
                "success": True,
                "message": generated.get("provider_notes", "Generation completed."),
                "duration_ms": int(generated.get("generation_duration_ms") or 0),
            }
        ]

    inserted = 0
    total_duration_ms = int(generated.get("generation_duration_ms") or 0)
    for index, attempt in enumerate(attempts, start=1):
        provider = str(attempt.get("provider") or "unknown")
        available = bool(attempt.get("available"))
        success = bool(attempt.get("success"))
        message = str(attempt.get("message") or "")
        duration_ms = int(attempt.get("duration_ms") or 0)
        conn.execute(
            """
            INSERT INTO ai_provider_logs (
                package_id, provider, available, success, message, duration_ms,
                attempt_order, generation_mode, provider_chain, total_generation_duration_ms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                package_id,
                provider,
                int(available),
                int(success),
                message,
                duration_ms,
                index,
                generated.get("generation_mode", "deterministic_template"),
                generated.get("provider_chain", "template"),
                total_duration_ms,
            ),
        )
        inserted += 1
    return inserted


def list_provider_logs(conn, limit: int = 100, package_id: int | None = None) -> list[dict[str, Any]]:
    limit = max(1, min(int(limit or 100), 500))
    params: list[Any] = []
    where = ""
    if package_id is not None:
        where = "WHERE l.package_id = ?"
        params.append(package_id)
    params.append(limit)
    rows = conn.execute(
        f"""
        SELECT l.*, cp.topic, cp.subject, cp.tone, cp.prompt_template_name, cp.provider_used AS final_provider
        FROM ai_provider_logs l
        LEFT JOIN content_packages cp ON cp.id = l.package_id
        {where}
        ORDER BY l.id DESC
        LIMIT ?
        """,
        params,
    ).fetchall()
    return [dict(row) for row in rows]


def build_provider_log_summary(conn) -> dict[str, Any]:
    logs = [dict(row) for row in conn.execute(
        """
        SELECT l.*, cp.topic, cp.subject, cp.tone, cp.prompt_template_name, cp.provider_used AS final_provider
        FROM ai_provider_logs l
        LEFT JOIN content_packages cp ON cp.id = l.package_id
        ORDER BY l.id DESC
        """
    ).fetchall()]

    package_rows = [dict(row) for row in conn.execute(
        """
        SELECT id, topic, subject, provider_used, generation_mode, provider_chain,
               provider_notes, provider_attempts, prompt_template_name, created_at
        FROM content_packages
        ORDER BY id DESC
        LIMIT 50
        """
    ).fetchall()]

    provider_stats: dict[str, dict[str, Any]] = {}
    for log in logs:
        name = log.get("provider") or "unknown"
        stat = provider_stats.setdefault(
            name,
            {
                "provider": name,
                "attempts": 0,
                "available_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "avg_duration_ms": 0,
                "total_duration_ms": 0,
                "last_message": "",
            },
        )
        stat["attempts"] += 1
        stat["available_count"] += int(bool(log.get("available")))
        stat["success_count"] += int(bool(log.get("success")))
        stat["failure_count"] += int(not bool(log.get("success")))
        stat["total_duration_ms"] += int(log.get("duration_ms") or 0)
        if not stat["last_message"]:
            stat["last_message"] = log.get("message") or ""

    for stat in provider_stats.values():
        attempts = max(stat["attempts"], 1)
        stat["success_rate_pct"] = round((stat["success_count"] / attempts) * 100, 1)
        stat["avg_duration_ms"] = round(stat["total_duration_ms"] / attempts, 1)

    latest_by_package = _latest_logs_grouped_by_package(logs)
    fallback_packages = []
    for package in package_rows:
        attempts = parse_provider_attempts(package.get("provider_attempts"))
        failed_before_template = any(
            (item.get("provider") != "template") and not bool(item.get("success"))
            for item in attempts
        )
        if package.get("provider_used") == "template" and failed_before_template:
            fallback_packages.append(package)

    recommendations = _build_recommendations(provider_stats.values(), fallback_packages, package_rows)

    return {
        "totals": {
            "total_logs": len(logs),
            "packages_logged": len({log.get("package_id") for log in logs if log.get("package_id") is not None}),
            "successes": sum(1 for log in logs if log.get("success")),
            "failures": sum(1 for log in logs if not log.get("success")),
            "fallback_to_template_count": len(fallback_packages),
        },
        "provider_stats": sorted(provider_stats.values(), key=lambda item: (item["success_rate_pct"], item["attempts"]), reverse=True),
        "recent_logs": logs[:50],
        "latest_by_package": latest_by_package[:20],
        "fallback_packages": fallback_packages[:20],
        "recommendations": recommendations,
        "report_markdown": build_provider_report_markdown(provider_stats.values(), logs[:50], fallback_packages[:20], recommendations),
    }


def _latest_logs_grouped_by_package(logs: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for log in logs:
        package_id = log.get("package_id")
        if package_id is not None:
            grouped[int(package_id)].append(log)
    result = []
    for package_id, items in grouped.items():
        first = items[0]
        result.append(
            {
                "package_id": package_id,
                "topic": first.get("topic") or "",
                "final_provider": first.get("final_provider") or "",
                "attempts": sorted(items, key=lambda item: int(item.get("attempt_order") or 0)),
            }
        )
    return result


def _build_recommendations(provider_stats: Iterable[dict[str, Any]], fallback_packages: list[dict[str, Any]], package_rows: list[dict[str, Any]]) -> list[str]:
    recommendations = []
    stats = list(provider_stats)
    ollama = next((item for item in stats if item["provider"] == "ollama"), None)
    transformers = next((item for item in stats if item["provider"] == "transformers"), None)
    template = next((item for item in stats if item["provider"] == "template"), None)

    if fallback_packages:
        recommendations.append(
            f"{len(fallback_packages)} recent package(s) fell back to template after another provider failed. Keep template fallback enabled."
        )
    if ollama and ollama["failure_count"] > 0:
        recommendations.append("Ollama has failures. Keep USE_OLLAMA=false on this laptop until it is installed on the desktop.")
    if transformers and transformers["failure_count"] > 0:
        recommendations.append("Transformers has failures. Enable it only after installing compatible transformers/torch packages.")
    if template and template["success_count"] > 0:
        recommendations.append("Template provider is working. This is good for daily Shorts workflow when local AI tools are unavailable.")
    if not package_rows:
        recommendations.append("Generate at least one content package to see provider logs and fallback behavior.")
    if not recommendations:
        recommendations.append("Provider chain looks stable. Continue generating packages and monitor this page after enabling new AI tools.")
    return recommendations


def build_provider_report_markdown(provider_stats: Iterable[dict[str, Any]], recent_logs: list[dict[str, Any]], fallback_packages: list[dict[str, Any]], recommendations: list[str]) -> str:
    stat_lines = []
    for stat in provider_stats:
        stat_lines.append(
            f"- {stat['provider']}: {stat['success_count']}/{stat['attempts']} success "
            f"({stat['success_rate_pct']}%), avg {stat['avg_duration_ms']} ms"
        )
    if not stat_lines:
        stat_lines.append("- No provider logs yet.")

    log_lines = []
    for log in recent_logs[:20]:
        status = "success" if log.get("success") else "failed"
        log_lines.append(
            f"- Package #{log.get('package_id')} | {log.get('provider')} | {status} | {log.get('message', '')}"
        )
    if not log_lines:
        log_lines.append("- No recent attempts yet.")

    fallback_lines = []
    for package in fallback_packages[:20]:
        fallback_lines.append(f"- Package #{package.get('id')}: {package.get('topic')} → template fallback")
    if not fallback_lines:
        fallback_lines.append("- No fallback-to-template packages detected yet.")

    return "\n".join([
        "# AI Provider Fallback Report",
        "",
        "## Provider performance",
        *stat_lines,
        "",
        "## Recent attempts",
        *log_lines,
        "",
        "## Template fallback packages",
        *fallback_lines,
        "",
        "## Recommended actions",
        *(f"- {item}" for item in recommendations),
        "",
    ])
