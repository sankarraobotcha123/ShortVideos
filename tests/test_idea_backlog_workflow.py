from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def test_content_idea_backlog_scoring_and_conversion(tmp_path):
    settings.database_path = tmp_path / "idea-backlog-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)
    payload = {
        "title": "Why do we see lightning before thunder?",
        "subject": "Science",
        "class_level": "Class 7",
        "target_audience": "School students",
        "language": "English",
        "idea_type": "curiosity",
        "hook_angle": "Most students think they happen at different times, but it is about speed.",
        "source_hint": "Light travels faster than sound, so lightning reaches our eyes first.",
        "status": "ready",
        "notes": "Good visual with lightning flash and sound wave.",
        "curiosity_score": 9,
        "evergreen_score": 8,
        "visual_potential_score": 9,
        "student_value_score": 8,
        "production_effort_score": 4,
        "monetization_potential_score": 6,
    }

    created = client.post("/api/content-ideas", json=payload)
    assert created.status_code == 201
    idea = created.json()["idea"]
    assert idea["total_score"] >= 80
    assert idea["priority"] == "high"

    listed = client.get("/api/content-ideas")
    assert listed.status_code == 200
    assert listed.json()["idea_backlog"]["summary"]["total"] == 1

    updated = client.patch(f"/api/content-ideas/{idea['id']}", json={**payload, "status": "shortlisted", "production_effort_score": 5})
    assert updated.status_code == 200
    assert updated.json()["idea"]["status"] == "shortlisted"

    converted = client.post(f"/api/content-ideas/{idea['id']}/convert", json={"duration_seconds": 60, "tone": "Curious"})
    assert converted.status_code == 201
    assert converted.json()["package"]["topic"] == payload["title"]
    assert converted.json()["idea"]["status"] == "converted"
    assert converted.json()["idea"]["converted_package_id"] == converted.json()["package"]["id"]

    download = client.get("/content-ideas/download")
    assert download.status_code == 200
    assert b"Content Idea Backlog" in download.content
