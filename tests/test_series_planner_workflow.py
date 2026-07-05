from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def test_content_series_planner_workflow(tmp_path):
    settings.database_path = tmp_path / "series-planner-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)

    series_payload = {
        "title": "Why does nature work like this?",
        "niche": "Class 6-8 Science curiosity Shorts",
        "target_audience": "School students",
        "subject": "Science",
        "class_level": "Class 7",
        "language": "English",
        "series_goal": "Create connected curiosity Shorts.",
        "status": "planning",
        "planned_count": 5,
        "episode_style": "Curiosity hook then simple explanation.",
        "cta_strategy": "End by teasing the next episode.",
        "notes": "Demo series.",
    }
    created = client.post("/api/content-series", json=series_payload)
    assert created.status_code == 201
    series = created.json()["series"]
    assert series["title"] == series_payload["title"]

    idea = client.post(
        "/api/content-ideas",
        json={
            "title": "Why are leaves green?",
            "subject": "Science",
            "class_level": "Class 7",
            "target_audience": "School students",
            "language": "English",
            "idea_type": "curiosity",
            "hook_angle": "Start with a leaf and reveal chlorophyll.",
            "source_hint": "Chlorophyll reflects green light.",
            "status": "ready",
            "curiosity_score": 8,
            "evergreen_score": 8,
            "visual_potential_score": 8,
            "student_value_score": 8,
            "production_effort_score": 4,
            "monetization_potential_score": 6,
        },
    )
    assert idea.status_code == 201
    idea_id = idea.json()["idea"]["id"]

    item = client.post(
        f"/api/content-series/{series['id']}/items",
        json={
            "idea_id": idea_id,
            "order_index": 1,
            "episode_title": "Why are leaves green?",
            "hook_angle": "Start from something students see daily.",
            "target_status": "idea_ready",
            "notes": "First episode.",
        },
    )
    assert item.status_code == 201
    item_id = item.json()["series_item"]["id"]

    detail = client.get(f"/api/content-series/{series['id']}")
    assert detail.status_code == 200
    assert len(detail.json()["items"]) == 1

    updated = client.patch(
        f"/api/content-series/{series['id']}/items/{item_id}",
        json={
            "idea_id": idea_id,
            "order_index": 2,
            "episode_title": "Why are leaves green?",
            "hook_angle": "Connect leaf color to food-making.",
            "target_status": "planned",
            "notes": "Moved after intro episode.",
        },
    )
    assert updated.status_code == 200
    assert updated.json()["series_item"]["order_index"] == 2

    download = client.get("/content-series/download")
    assert download.status_code == 200
    assert b"Content Series Planner" in download.content

    single = client.get(f"/content-series/{series['id']}/download")
    assert single.status_code == 200
    assert b"Series Plan" in single.content
