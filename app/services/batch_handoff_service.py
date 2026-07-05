from __future__ import annotations

import csv
import json
import re
import zipfile
from io import StringIO
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.services.export_service import export_package


def _safe_slug(value: str) -> str:
    value = (value or "production-handoff").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:90] or "production-handoff"


def _rows(conn, sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def _one(conn, sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    row = conn.execute(sql, params).fetchone()
    return dict(row) if row else None


def _package_context(conn, package_id: int) -> dict[str, list[dict[str, Any]]]:
    return {
        "audio_assets": _rows(conn, "SELECT * FROM audio_assets WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "assembly_plans": _rows(conn, "SELECT * FROM assembly_plans WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "video_drafts": _rows(conn, "SELECT * FROM video_drafts WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "thumbnail_guides": _rows(conn, "SELECT * FROM thumbnail_guides WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "source_safety_reviews": _rows(conn, "SELECT * FROM source_safety_reviews WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "trust_reviews": _rows(conn, "SELECT * FROM teacher_trust_reviews WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "learning_outputs": _rows(conn, "SELECT * FROM learning_outputs WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "publishing_approvals": _rows(conn, "SELECT * FROM publishing_approvals WHERE package_id = ? ORDER BY id DESC", (package_id,)),
        "provider_logs": _rows(conn, "SELECT * FROM ai_provider_logs WHERE package_id = ? ORDER BY attempt_order ASC, id ASC", (package_id,)),
    }


def _visual_assets(conn) -> list[dict[str, Any]]:
    return _rows(conn, "SELECT * FROM visual_assets ORDER BY id DESC")


def _select_packages(conn, *, batch_id: int | None, ready_only: bool, limit_count: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    where = []
    params: list[Any] = []
    if batch_id is not None:
        where.append("cp.batch_id = ?")
        params.append(batch_id)
    where_sql = f"WHERE {' AND '.join(where)}" if where else ""
    limit_count = max(1, min(int(limit_count or 50), 300))

    packages = _rows(
        conn,
        f"""
        SELECT
            cp.*,
            b.name AS batch_name,
            pc.planned_publish_date,
            pc.status AS calendar_status,
            pa.status AS publishing_approval_status,
            pa.gate_status AS publishing_gate_status,
            pa.reviewer_decision AS publishing_reviewer_decision,
            ss.risk_level AS latest_source_risk,
            tt.overall_trust_score AS latest_trust_score,
            tt.reviewer_decision AS latest_trust_decision
        FROM content_packages cp
        LEFT JOIN content_batches b ON b.id = cp.batch_id
        LEFT JOIN publishing_calendar pc ON pc.package_id = cp.id
        LEFT JOIN publishing_approvals pa ON pa.id = (
            SELECT id FROM publishing_approvals WHERE package_id = cp.id ORDER BY id DESC LIMIT 1
        )
        LEFT JOIN source_safety_reviews ss ON ss.id = (
            SELECT id FROM source_safety_reviews WHERE package_id = cp.id ORDER BY id DESC LIMIT 1
        )
        LEFT JOIN teacher_trust_reviews tt ON tt.id = (
            SELECT id FROM teacher_trust_reviews WHERE package_id = cp.id ORDER BY id DESC LIMIT 1
        )
        {where_sql}
        ORDER BY COALESCE(pc.planned_publish_date, cp.created_at) ASC, cp.id ASC
        LIMIT ?
        """,
        tuple(params + [limit_count]),
    )

    selected: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for package in packages:
        readiness = _handoff_readiness(package)
        package["handoff_readiness"] = readiness
        if ready_only and not readiness["ready"]:
            skipped.append({
                "id": package.get("id"),
                "topic": package.get("topic"),
                "reason": readiness["reason"],
                "score": readiness["score"],
            })
            continue
        selected.append(package)
    return selected, skipped


def _handoff_readiness(package: dict[str, Any]) -> dict[str, Any]:
    score = 0
    reasons = []
    if package.get("review_status") in {"approved", "published"}:
        score += 25
    else:
        reasons.append("script not approved")

    trust_score = int(package.get("latest_trust_score") or package.get("trust_score") or 0)
    if trust_score >= 85:
        score += 25
    elif trust_score >= 70:
        score += 12
        reasons.append("trust score is below publish-ready threshold")
    else:
        reasons.append("trust score is low")

    if (package.get("latest_source_risk") or "") in {"low", "medium"}:
        score += 20
    else:
        reasons.append("source safety is missing or high risk")

    if package.get("publishing_approval_status") == "approved" and package.get("publishing_reviewer_decision") == "approved":
        score += 20
    else:
        reasons.append("publishing gate is not approved")

    if package.get("calendar_status"):
        score += 10
    else:
        reasons.append("not scheduled")

    ready = score >= 70 and package.get("review_status") in {"approved", "published"}
    if not reasons:
        reason = "ready for editor/publisher handoff"
    else:
        reason = "; ".join(reasons)
    return {"score": score, "ready": ready, "reason": reason}


def build_handoff_markdown(*, handoff_name: str, selected: list[dict[str, Any]], skipped: list[dict[str, Any]], ready_only: bool, batch_name: str = "") -> str:
    lines = [
        f"# Batch Production Handoff: {handoff_name}",
        "",
        f"- Batch: {batch_name or 'All selected packages'}",
        f"- Ready-only filter: {'Yes' if ready_only else 'No'}",
        f"- Included packages: {len(selected)}",
        f"- Skipped packages: {len(skipped)}",
        "",
        "## Editor workflow",
        "",
        "1. Open `manifest.csv` first.",
        "2. Work package-by-package in the recommended order.",
        "3. Use each package ZIP for script, subtitles, assembly plan, thumbnail guide, source safety, trust review, and draft video files.",
        "4. Finish edits in CapCut/Canva/manual editor.",
        "5. Update the publishing calendar and analytics after upload.",
        "",
        "## Included packages",
        "",
    ]
    if not selected:
        lines.append("No packages matched this handoff selection.")
    for item in selected:
        readiness = item.get("handoff_readiness") or {}
        lines.extend([
            f"### #{item.get('id')} — {item.get('topic')}",
            f"- Subject/Class: {item.get('subject')} / {item.get('class_level')}",
            f"- Batch: {item.get('batch_name') or 'No batch'}",
            f"- Calendar: {item.get('planned_publish_date') or 'Not scheduled'} ({item.get('calendar_status') or 'no status'})",
            f"- Review: {item.get('review_status')}; trust: {item.get('latest_trust_score') or item.get('trust_score')}",
            f"- Handoff score: {readiness.get('score', 0)} — {readiness.get('reason', '')}",
            "",
        ])
    lines.extend(["", "## Skipped packages", ""])
    if not skipped:
        lines.append("None.")
    else:
        lines.extend(f"- #{item.get('id')} {item.get('topic')}: {item.get('reason')}" for item in skipped)
    lines.extend([
        "",
        "## Handoff rule",
        "",
        "Do not publish directly from the handoff ZIP. Final publishing still needs the publishing approval gate and calendar status to be correct.",
    ])
    return "\n".join(lines) + "\n"


def _manifest_csv(selected: list[dict[str, Any]]) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=[
            "package_id",
            "topic",
            "subject",
            "class_level",
            "batch_name",
            "planned_publish_date",
            "calendar_status",
            "review_status",
            "trust_score",
            "source_risk",
            "publishing_gate",
            "handoff_score",
            "handoff_reason",
            "package_zip",
        ],
    )
    writer.writeheader()
    for item in selected:
        readiness = item.get("handoff_readiness") or {}
        writer.writerow({
            "package_id": item.get("id"),
            "topic": item.get("topic"),
            "subject": item.get("subject"),
            "class_level": item.get("class_level"),
            "batch_name": item.get("batch_name") or "",
            "planned_publish_date": item.get("planned_publish_date") or "",
            "calendar_status": item.get("calendar_status") or "",
            "review_status": item.get("review_status") or "",
            "trust_score": item.get("latest_trust_score") or item.get("trust_score") or 0,
            "source_risk": item.get("latest_source_risk") or "",
            "publishing_gate": item.get("publishing_approval_status") or "",
            "handoff_score": readiness.get("score", 0),
            "handoff_reason": readiness.get("reason", ""),
            "package_zip": f"packages/package-{item.get('id')}.zip",
        })
    return buffer.getvalue()


def create_batch_handoff(
    conn,
    *,
    handoff_name: str,
    batch_id: int | None = None,
    ready_only: bool = True,
    limit_count: int = 50,
    created_by: str = "",
    notes: str = "",
) -> dict[str, Any]:
    if batch_id is not None:
        batch = _one(conn, "SELECT * FROM content_batches WHERE id = ?", (batch_id,))
        if batch is None:
            raise ValueError("Batch not found")
        batch_name = batch.get("name", "")
    else:
        batch_name = ""

    selected, skipped = _select_packages(conn, batch_id=batch_id, ready_only=ready_only, limit_count=limit_count)
    settings.handoff_dir.mkdir(parents=True, exist_ok=True)
    slug = _safe_slug(handoff_name or batch_name or "production-handoff")
    run_dir = settings.handoff_dir / f"handoff-{slug}"
    run_dir.mkdir(parents=True, exist_ok=True)
    packages_dir = run_dir / "packages"
    packages_dir.mkdir(exist_ok=True)

    visual_assets = _visual_assets(conn)
    package_zip_entries: list[dict[str, Any]] = []
    for package in selected:
        context = _package_context(conn, int(package["id"]))
        package_zip = export_package(
            package,
            context["audio_assets"],
            context["assembly_plans"],
            context["video_drafts"],
            visual_assets,
            context["thumbnail_guides"],
            context["source_safety_reviews"],
            context["trust_reviews"],
            context["learning_outputs"],
            context["publishing_approvals"],
            context["provider_logs"],
        )
        target = packages_dir / f"package-{package['id']}.zip"
        target.write_bytes(Path(package_zip).read_bytes())
        package_zip_entries.append({"package_id": package["id"], "topic": package.get("topic"), "zip_file": str(target.relative_to(run_dir))})

    manifest = {
        "handoff_name": handoff_name,
        "batch_id": batch_id,
        "batch_name": batch_name,
        "ready_only": bool(ready_only),
        "package_count": len(selected),
        "skipped_count": len(skipped),
        "created_by": created_by,
        "notes": notes,
        "packages": selected,
        "package_zips": package_zip_entries,
        "skipped": skipped,
    }
    report = build_handoff_markdown(
        handoff_name=handoff_name,
        selected=selected,
        skipped=skipped,
        ready_only=ready_only,
        batch_name=batch_name,
    )
    (run_dir / "README_HANDOFF.md").write_text(report, encoding="utf-8")
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / "manifest.csv").write_text(_manifest_csv(selected), encoding="utf-8")
    (run_dir / "skipped_packages.json").write_text(json.dumps(skipped, indent=2, ensure_ascii=False), encoding="utf-8")

    zip_name = f"handoff-{slug}.zip"
    zip_path = settings.handoff_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in run_dir.rglob("*"):
            if file.is_file():
                zf.write(file, arcname=file.relative_to(run_dir))

    cursor = conn.execute(
        """
        INSERT INTO batch_handoff_runs (
            batch_id, handoff_name, ready_only, package_count, skipped_count,
            file_path, file_name, manifest_json, created_by, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            batch_id,
            handoff_name,
            int(bool(ready_only)),
            len(selected),
            len(skipped),
            str(zip_path),
            zip_name,
            json.dumps(manifest, ensure_ascii=False),
            created_by.strip(),
            notes.strip(),
        ),
    )
    run_id = int(cursor.lastrowid)
    run = _one(conn, "SELECT * FROM batch_handoff_runs WHERE id = ?", (run_id,))
    if run:
        run["manifest"] = manifest
    return run or {}


def list_batch_handoff_runs(conn, limit: int = 50) -> list[dict[str, Any]]:
    rows = _rows(
        conn,
        """
        SELECT bhr.*, b.name AS batch_name
        FROM batch_handoff_runs bhr
        LEFT JOIN content_batches b ON b.id = bhr.batch_id
        ORDER BY bhr.id DESC
        LIMIT ?
        """,
        (max(1, min(int(limit or 50), 200)),),
    )
    for row in rows:
        try:
            row["manifest"] = json.loads(row.get("manifest_json") or "{}")
        except Exception:
            row["manifest"] = {}
    return rows


def build_latest_handoff_report(conn) -> str:
    runs = list_batch_handoff_runs(conn, limit=25)
    lines = ["# Batch Export and Production Handoff Report", ""]
    if not runs:
        lines.append("No handoff exports have been created yet.")
        return "\n".join(lines) + "\n"
    for run in runs:
        lines.extend([
            f"## Run #{run.get('id')} — {run.get('handoff_name')}",
            f"- Batch: {run.get('batch_name') or 'All selected packages'}",
            f"- Packages: {run.get('package_count')} included, {run.get('skipped_count')} skipped",
            f"- Ready only: {'Yes' if run.get('ready_only') else 'No'}",
            f"- Created by: {run.get('created_by') or 'Not specified'}",
            f"- File: {run.get('file_name')}",
            "",
        ])
    return "\n".join(lines) + "\n"
