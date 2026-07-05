from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def _package_payload(topic: str, batch_id: int | None = None) -> dict:
    return {
        "board_source": "Self-written",
        "class_level": "Class 7",
        "subject": "Science",
        "topic": topic,
        "audience": "School students",
        "language": "English",
        "duration_seconds": 60,
        "output_type": "Short",
        "tone": "Curious",
        "source_notes": f"Self-written notes for {topic}.",
        "source_name": "Self notes",
        "source_license_type": "Original",
        "transformation_notes": "Original explanation with visual flow.",
        "batch_id": batch_id,
    }


def test_calendar_bulk_schedule_preview_and_apply(tmp_path):
    settings.database_path = tmp_path / "bulk-calendar-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)
    batch = client.post(
        "/api/batches",
        json={
            "name": "Bulk schedule test batch",
            "niche": "Science Shorts",
            "target_audience": "School students",
            "start_date": "2026-07-05",
            "planned_count": 3,
            "status": "planning",
            "notes": "Test batch",
        },
    )
    assert batch.status_code == 201
    batch_id = batch.json()["batch"]["id"]

    for topic in ["Why are leaves green?", "Why does thunder sound later?", "Why do magnets attract?"]:
        created = client.post("/api/content/generate", json=_package_payload(topic, batch_id))
        assert created.status_code == 201

    preview = client.post(
        "/api/calendar/bulk-schedule",
        json={
            "start_date": "2026-07-10",
            "batch_id": batch_id,
            "limit": 3,
            "videos_per_day": 2,
            "days_between": 1,
            "platform": "YouTube Shorts",
            "playlist_name": "Science Curiosity Shorts",
            "status": "planned",
            "order_by": "created_at",
            "apply": False,
        },
    )
    assert preview.status_code == 200
    preview_body = preview.json()["bulk_schedule"]
    assert preview_body["mode"] == "preview"
    assert preview_body["scheduled_count"] == 3
    assert [item["planned_publish_date"] for item in preview_body["items"]] == [
        "2026-07-10",
        "2026-07-10",
        "2026-07-12",
    ]

    applied = client.post(
        "/api/calendar/bulk-schedule",
        json={**preview_body, "apply": True},
    )
    assert applied.status_code == 200
    applied_body = applied.json()["bulk_schedule"]
    assert applied_body["mode"] == "applied"
    assert applied_body["inserted_count"] == 3

    calendar = client.get("/api/calendar")
    assert calendar.status_code == 200
    assert len(calendar.json()["calendar"]) == 3

    runs = client.get("/api/calendar/bulk-runs")
    assert runs.status_code == 200
    assert runs.json()["bulk_runs"][0]["scheduled_count"] == 3

    report = client.get("/calendar/bulk-schedule/download")
    assert report.status_code == 200
    assert b"Content Calendar Bulk Scheduling Report" in report.content
