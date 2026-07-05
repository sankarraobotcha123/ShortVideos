from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def _payload(topic: str, batch_id: int | None = None) -> dict:
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


def test_batch_handoff_export_includes_package_zip_and_manifest(tmp_path):
    settings.database_path = tmp_path / "handoff-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.handoff_dir = tmp_path / "handoffs"
    init_db()

    client = TestClient(app)
    batch = client.post(
        "/api/batches",
        json={
            "name": "Handoff test batch",
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

    created = client.post("/api/content/generate", json=_payload("Why are leaves green?", batch_id))
    assert created.status_code == 201
    package_id = created.json()["package"]["id"]
    review = client.patch(
        f"/api/content/{package_id}/review",
        json={"review_status": "approved", "script_text": created.json()["package"]["script_text"], "reviewer_notes": "Approved for test."},
    )
    assert review.status_code == 200

    handoff = client.post(
        "/api/batch-handoffs",
        json={
            "handoff_name": "Handoff Test Export",
            "batch_id": batch_id,
            "ready_only": False,
            "limit_count": 5,
            "created_by": "tester@example.com",
            "notes": "Test handoff export.",
        },
    )
    assert handoff.status_code == 201
    run = handoff.json()["handoff_run"]
    assert run["package_count"] == 1
    assert run["file_name"].endswith(".zip")

    runs = client.get("/api/batch-handoffs")
    assert runs.status_code == 200
    assert runs.json()["handoff_runs"][0]["package_count"] == 1

    download = client.get(f"/batch-handoffs/{run['id']}/download")
    assert download.status_code == 200
    assert download.content.startswith(b"PK")

    report = client.get("/batch-handoffs/download")
    assert report.status_code == 200
    assert b"Batch Export and Production Handoff Report" in report.content
