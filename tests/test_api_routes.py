from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def test_react_api_generate_and_list(tmp_path):
    settings.database_path = tmp_path / "api-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)
    payload = {
        "board_source": "Self-written",
        "class_level": "Class 7",
        "subject": "Science",
        "topic": "Why are leaves green?",
        "audience": "School students",
        "language": "English",
        "duration_seconds": 60,
        "output_type": "Short",
        "tone": "Curious",
        "source_notes": "Leaves contain chlorophyll. Chlorophyll reflects green light.",
        "source_name": "Self notes",
        "source_license_type": "Original",
        "transformation_notes": "Original analogy added.",
    }

    created = client.post("/api/content/generate", json=payload)
    assert created.status_code == 201
    package_id = created.json()["package"]["id"]

    listed = client.get("/api/packages")
    assert listed.status_code == 200
    assert listed.json()["stats"]["total"] == 1

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert detail.json()["package"]["topic"] == "Why are leaves green?"
