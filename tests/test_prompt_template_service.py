from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def _base_payload(**overrides):
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
    payload.update(overrides)
    return payload


def test_prompt_templates_seed_list_preview_and_generate(tmp_path):
    settings.database_path = tmp_path / "prompt-template-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)

    listed = client.get("/api/prompt-templates?task_type=script")
    assert listed.status_code == 200
    templates = listed.json()["prompt_templates"]
    assert len(templates) >= 5
    template = templates[0]

    preview = client.post(f"/api/prompt-templates/{template['id']}/preview", json=_base_payload())
    assert preview.status_code == 200
    assert "rendered_text" in preview.json()["preview"]

    created = client.post("/api/content/generate", json=_base_payload(prompt_template_id=template["id"]))
    assert created.status_code == 201
    package = created.json()["package"]
    assert package["prompt_template_id"] == template["id"]
    assert package["prompt_template_name"] == template["name"]
    assert package["script_text"]

    exported = client.get(f"/content/{package['id']}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_prompt_template_crud_workflow(tmp_path):
    settings.database_path = tmp_path / "prompt-template-crud-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)
    payload = {
        "name": "Test Script Template",
        "task_type": "script",
        "style_key": "test_style",
        "template_text": "{hook}\n\nMain fact: {top_fact}.\n\nMemory line: {memory_line}.",
        "active": True,
        "notes": "Created during test.",
    }
    created = client.post("/api/prompt-templates", json=payload)
    assert created.status_code == 201
    template_id = created.json()["prompt_template"]["id"]

    updated_payload = {**payload, "name": "Updated Test Script Template", "active": False}
    updated = client.patch(f"/api/prompt-templates/{template_id}", json=updated_payload)
    assert updated.status_code == 200
    assert updated.json()["prompt_template"]["name"] == "Updated Test Script Template"
    assert updated.json()["prompt_template"]["active"] == 0

    deleted = client.delete(f"/api/prompt-templates/{template_id}")
    assert deleted.status_code == 200
    assert deleted.json()["deleted"] is True
