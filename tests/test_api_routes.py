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


def test_batch_and_calendar_workflow(tmp_path):
    settings.database_path = tmp_path / "batch-calendar-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)

    batch_payload = {
        "name": "First 20 Science Shorts",
        "niche": "Class 6-8 Science curiosity Shorts",
        "target_audience": "School students",
        "start_date": "2026-07-05",
        "end_date": "2026-07-25",
        "planned_count": 20,
        "status": "planning",
        "notes": "Batch test",
    }
    created_batch = client.post("/api/batches", json=batch_payload)
    assert created_batch.status_code == 201
    batch_id = created_batch.json()["batch"]["id"]

    package_payload = {
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
        "batch_id": batch_id,
    }
    created_package = client.post("/api/content/generate", json=package_payload)
    assert created_package.status_code == 201
    package_id = created_package.json()["package"]["id"]
    assert created_package.json()["package"]["batch_id"] == batch_id

    batch_detail = client.get(f"/api/batches/{batch_id}")
    assert batch_detail.status_code == 200
    assert batch_detail.json()["batch"]["completed_count"] == 1
    assert batch_detail.json()["packages"][0]["id"] == package_id

    scheduled = client.post("/api/calendar", json={
        "package_id": package_id,
        "planned_publish_date": "2026-07-06",
        "platform": "YouTube Shorts",
        "status": "planned",
        "playlist_name": "Science Curiosity Shorts",
        "notes": "Publish after review",
    })
    assert scheduled.status_code == 201
    assert scheduled.json()["calendar_entry"]["package_id"] == package_id

    calendar = client.get("/api/calendar")
    assert calendar.status_code == 200
    assert len(calendar.json()["calendar"]) == 1
    assert calendar.json()["calendar"][0]["topic"] == "Why are leaves green?"


def test_audio_manual_fallback_workflow(tmp_path):
    settings.database_path = tmp_path / "audio-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.audio_dir = tmp_path / "audio"
    settings.tts_provider_chain = ["manual_recording"]
    settings.use_windows_sapi = False
    settings.use_pyttsx3 = False
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

    audio = client.post(f"/api/content/{package_id}/audio")
    assert audio.status_code == 201
    asset = audio.json()["audio_asset"]
    assert asset["status"] == "manual_required"
    assert asset["provider_used"] == "manual_recording"
    assert asset["file_name"].endswith("recording-guide.txt")

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["audio_assets"]) == 1

    download = client.get(f"/content/{package_id}/audio/{asset['id']}/download")
    assert download.status_code == 200
    assert b"Narration Recording Guide" in download.content


def test_assembly_plan_workflow_and_export(tmp_path):
    settings.database_path = tmp_path / "assembly-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.audio_dir = tmp_path / "audio"
    settings.tts_provider_chain = ["manual_recording"]
    settings.use_windows_sapi = False
    settings.use_pyttsx3 = False
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

    audio = client.post(f"/api/content/{package_id}/audio")
    assert audio.status_code == 201

    assembly = client.post(f"/api/content/{package_id}/assembly")
    assert assembly.status_code == 201
    plan = assembly.json()["assembly_plan"]
    assert plan["scene_count"] == 5
    assert "CapCut / Manual Assembly Plan" in plan["plan_markdown"]

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["assembly_plans"]) == 1

    download = client.get(f"/content/{package_id}/assembly/{plan['id']}/download")
    assert download.status_code == 200
    assert b"Scene timeline" in download.content

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_video_draft_workflow_and_export(tmp_path):
    settings.database_path = tmp_path / "video-draft-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.audio_dir = tmp_path / "audio"
    settings.video_draft_dir = tmp_path / "video_drafts"
    settings.tts_provider_chain = ["manual_recording"]
    settings.use_windows_sapi = False
    settings.use_pyttsx3 = False
    init_db()

    client = TestClient(app)
    payload = {
        "board_source": "Self-written",
        "class_level": "Class 7",
        "subject": "Science",
        "topic": "Why are leaves green?",
        "audience": "School students",
        "language": "English",
        "duration_seconds": 20,
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

    assembly = client.post(f"/api/content/{package_id}/assembly")
    assert assembly.status_code == 201

    draft = client.post(f"/api/content/{package_id}/video-draft")
    assert draft.status_code == 201
    video_draft = draft.json()["video_draft"]
    assert video_draft["status"] in {"generated", "manual_required"}
    assert video_draft["file_name"]

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["video_drafts"]) == 1

    download = client.get(f"/content/{package_id}/video-draft/{video_draft['id']}/download")
    assert download.status_code == 200

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"
