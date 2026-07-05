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


def test_visual_asset_upload_and_video_draft_matching(tmp_path):
    settings.database_path = tmp_path / "asset-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.audio_dir = tmp_path / "audio"
    settings.video_draft_dir = tmp_path / "video_drafts"
    settings.asset_library_dir = tmp_path / "asset_library"
    settings.tts_provider_chain = ["manual_recording"]
    settings.use_windows_sapi = False
    settings.use_pyttsx3 = False
    init_db()

    client = TestClient(app)

    from io import BytesIO
    from PIL import Image

    image_buffer = BytesIO()
    Image.new("RGB", (256, 256), (34, 197, 94)).save(image_buffer, format="PNG")
    image_buffer.seek(0)

    uploaded = client.post(
        "/api/assets",
        data={
            "title": "Leaf chlorophyll icon",
            "tags": "leaf, chlorophyll, photosynthesis, science",
            "description": "Reusable visual for green leaves.",
            "source_type": "self_created",
            "license_type": "Original",
            "notes": "Test asset",
        },
        files={"file": ("leaf.png", image_buffer, "image/png")},
    )
    assert uploaded.status_code == 201
    asset_id = uploaded.json()["asset"]["id"]

    listed = client.get("/api/assets")
    assert listed.status_code == 200
    assert len(listed.json()["assets"]) == 1

    package_payload = {
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
    created = client.post("/api/content/generate", json=package_payload)
    assert created.status_code == 201
    package_id = created.json()["package"]["id"]

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert detail.json()["suggested_visual_assets"][0]["id"] == asset_id

    draft = client.post(f"/api/content/{package_id}/video-draft")
    assert draft.status_code == 201
    assert draft.json()["video_draft"]["status"] in {"generated", "manual_required"}

    downloaded = client.get(f"/assets/{asset_id}/download")
    assert downloaded.status_code == 200
    assert downloaded.headers["content-type"].startswith("image/")


def test_thumbnail_helper_workflow_and_export(tmp_path):
    settings.database_path = tmp_path / "thumbnail-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.thumbnail_dir = tmp_path / "thumbnails"
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

    thumbnail = client.post(f"/api/content/{package_id}/thumbnail")
    assert thumbnail.status_code == 201
    guide = thumbnail.json()["thumbnail_guide"]
    assert guide["status"] == "generated"
    assert "Canva" in guide["canva_prompt"] or "thumbnail" in guide["canva_prompt"].lower()

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["thumbnail_guides"]) == 1

    download = client.get(f"/content/{package_id}/thumbnail/{guide['id']}/download")
    assert download.status_code == 200
    assert b"Thumbnail Helper" in download.content

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_source_safety_workflow_and_export(tmp_path):
    settings.database_path = tmp_path / "source-safety-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.source_safety_dir = tmp_path / "source_safety"
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
        "page_or_section_reference": "Self-written concept note",
        "transformation_notes": "Original analogy, example, and visual flow added.",
    }
    created = client.post("/api/content/generate", json=payload)
    assert created.status_code == 201
    package_id = created.json()["package"]["id"]

    review = client.post(f"/api/content/{package_id}/source-safety")
    assert review.status_code == 201
    item = review.json()["source_safety_review"]
    assert item["risk_level"] in {"low", "medium", "high"}
    assert item["file_name"].endswith("source-safety-review.md")

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["source_safety_reviews"]) == 1

    download = client.get(f"/content/{package_id}/source-safety/{item['id']}/download")
    assert download.status_code == 200
    assert b"Source Safety" in download.content

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_teacher_trust_review_workflow_and_export(tmp_path):
    settings.database_path = tmp_path / "trust-review-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.source_safety_dir = tmp_path / "source_safety"
    settings.trust_review_dir = tmp_path / "trust_reviews"
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
        "page_or_section_reference": "Self-written concept note",
        "transformation_notes": "Original analogy, example, and visual flow added.",
    }
    created = client.post("/api/content/generate", json=payload)
    assert created.status_code == 201
    package_id = created.json()["package"]["id"]

    safety = client.post(f"/api/content/{package_id}/source-safety")
    assert safety.status_code == 201

    trust = client.post(f"/api/content/{package_id}/trust-review")
    assert trust.status_code == 201
    review = trust.json()["trust_review"]
    assert 0 <= review["overall_trust_score"] <= 100
    assert review["file_name"].endswith("teacher-trust-review.md")
    assert trust.json()["package"]["trust_score"] == review["overall_trust_score"]

    updated = client.patch(
        f"/api/content/{package_id}/trust-review/{review['id']}",
        json={
            "factual_accuracy_score": 90,
            "age_appropriateness_score": 88,
            "simplicity_score": 92,
            "visual_clarity_score": 84,
            "engagement_score": 86,
            "source_safety_score": 91,
            "reviewer_confidence_score": 93,
            "reviewer_decision": "approved",
            "reviewer_notes": "Reviewed and ready after final subtitle check.",
            "checklist_json": review["checklist_json"],
        },
    )
    assert updated.status_code == 200
    updated_review = updated.json()["trust_review"]
    assert updated_review["reviewer_decision"] == "approved"
    assert updated_review["overall_trust_score"] >= 85

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["trust_reviews"]) == 1

    download = client.get(f"/content/{package_id}/trust-review/{review['id']}/download")
    assert download.status_code == 200
    assert b"Teacher Trust Score Review" in download.content

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_learning_output_workflow_and_export(tmp_path):
    settings.database_path = tmp_path / "learning-output-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.learning_output_dir = tmp_path / "learning_outputs"
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
        "source_notes": "Leaves contain chlorophyll. Chlorophyll absorbs sunlight. Chlorophyll reflects green light.",
        "source_name": "Self notes",
        "source_license_type": "Original",
        "page_or_section_reference": "Self-written concept note",
        "transformation_notes": "Original analogy, example, and visual flow added.",
    }
    created = client.post("/api/content/generate", json=payload)
    assert created.status_code == 201
    package_id = created.json()["package"]["id"]

    output = client.post(f"/api/content/{package_id}/learning-output")
    assert output.status_code == 201
    item = output.json()["learning_output"]
    assert item["status"] == "generated"
    assert item["file_name"].endswith(".md")
    assert "Revision Notes" in item["revision_notes_markdown"]
    assert "Worksheet" in item["worksheet_markdown"]
    assert "flashcards" not in item  # API stores flashcards_json, not nested object

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    assert len(detail.json()["learning_outputs"]) == 1

    download = client.get(f"/content/{package_id}/learning-output/{item['id']}/download")
    assert download.status_code == 200
    assert b"Learning Output Pack" in download.content

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_analytics_dashboard_insights_workflow(tmp_path):
    settings.database_path = tmp_path / "analytics-insights-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)

    packages = []
    for topic, tone, views, retention in [
        ("Why are leaves green?", "Curious", 1500, 78),
        ("Why does ice float?", "Story-based", 2400, 86),
        ("Common photosynthesis mistake", "Mistake correction", 350, 42),
    ]:
        created = client.post(
            "/api/content/generate",
            json={
                "board_source": "Self-written",
                "class_level": "Class 7",
                "subject": "Science",
                "topic": topic,
                "audience": "School students",
                "language": "English",
                "duration_seconds": 60,
                "output_type": "Short",
                "tone": tone,
                "source_notes": "Simple self-written science facts for testing.",
                "source_name": "Self notes",
                "source_license_type": "Original",
                "transformation_notes": "Original analogy added.",
            },
        )
        assert created.status_code == 201
        package_id = created.json()["package"]["id"]
        packages.append(package_id)
        analytics = client.post(
            f"/api/content/{package_id}/analytics",
            json={
                "platform": "YouTube Shorts",
                "entry_date": "2026-07-05",
                "views": views,
                "likes": max(1, views // 20),
                "comments": max(1, views // 100),
                "shares": max(1, views // 80),
                "avg_view_duration_seconds": 31,
                "retention_pct": retention,
                "ctr_pct": 5.5,
                "notes": "Test analytics entry",
            },
        )
        assert analytics.status_code == 201

    insights = client.get("/api/analytics/insights")
    assert insights.status_code == 200
    body = insights.json()
    assert body["totals"]["packages_with_analytics"] == 3
    assert body["totals"]["total_latest_views"] == 4250
    assert body["top_videos_by_views"][0]["topic"] == "Why does ice float?"
    assert body["top_videos_by_retention"][0]["retention_pct"] == 86
    assert body["weak_videos"]
    assert body["grouped"]["tones"]
    assert "Analytics Dashboard Insights" in body["report_markdown"]


def test_ai_provider_logging_workflow(tmp_path):
    settings.database_path = tmp_path / "provider-log-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.ai_provider_chain = ["transformers", "template"]
    settings.use_ollama = False
    settings.use_transformers = False
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

    detail = client.get(f"/api/content/{package_id}")
    assert detail.status_code == 200
    provider_logs = detail.json()["provider_logs"]
    assert len(provider_logs) >= 2
    assert provider_logs[-1]["provider"] == "template"
    assert provider_logs[-1]["success"] == 1

    logs = client.get("/api/provider-logs")
    assert logs.status_code == 200
    body = logs.json()
    assert body["summary"]["totals"]["packages_logged"] >= 1
    assert body["summary"]["provider_stats"]
    assert "AI Provider Fallback Report" in body["summary"]["report_markdown"]

    exported = client.get(f"/content/{package_id}/export")
    assert exported.status_code == 200
    assert exported.headers["content-type"] == "application/zip"


def test_demo_seed_and_readiness_workflow(tmp_path):
    settings.database_path = tmp_path / "demo-seed-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.audio_dir = tmp_path / "audio"
    settings.video_draft_dir = tmp_path / "video_drafts"
    settings.asset_library_dir = tmp_path / "asset_library"
    settings.thumbnail_dir = tmp_path / "thumbnails"
    settings.source_safety_dir = tmp_path / "source_safety"
    settings.trust_review_dir = tmp_path / "trust_reviews"
    settings.learning_output_dir = tmp_path / "learning_outputs"
    settings.ai_provider_chain = ["transformers", "template"]
    settings.use_ollama = False
    settings.use_transformers = False
    init_db()

    client = TestClient(app)

    before = client.get("/api/system/readiness")
    assert before.status_code == 200
    assert before.json()["readiness"]["overall_ready"] is True

    seeded = client.post("/api/demo/seed", json={"reset_demo": False})
    assert seeded.status_code == 201
    body = seeded.json()
    assert body["demo"]["created"] is True
    assert body["demo"]["package_count"] == 3
    assert body["readiness"]["demo_seeded"] is True

    packages = client.get("/api/packages")
    assert packages.status_code == 200
    assert packages.json()["stats"]["total"] == 3

    insights = client.get("/api/analytics/insights")
    assert insights.status_code == 200
    assert insights.json()["totals"]["packages_with_analytics"] == 3

    duplicate = client.post("/api/demo/seed", json={"reset_demo": False})
    assert duplicate.status_code == 201
    assert duplicate.json()["demo"]["created"] is False
    assert duplicate.json()["demo"]["package_count"] == 3

    reset = client.post("/api/demo/seed", json={"reset_demo": True})
    assert reset.status_code == 201
    assert reset.json()["demo"]["created"] is True
    assert reset.json()["demo"]["package_count"] == 3


def test_release_checklist_api_available(tmp_path):
    settings.database_path = tmp_path / "release-check-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)
    response = client.get("/api/release/checklist")
    assert response.status_code == 200
    body = response.json()["release"]
    assert body["commit_message"] == "Add permission aware frontend action guards"
    assert "git status" in body["git_commands"]
    assert body["report_markdown"].startswith("# Production Cleanup")

    download = client.get("/release/checklist/download")
    assert download.status_code == 200
    assert b"Production Cleanup and Release Checklist" in download.content


def test_setup_guide_api(tmp_path):
    settings.database_path = tmp_path / "setup-guide-test.db"
    init_db()

    client = TestClient(app)
    response = client.get("/api/setup/guide")
    assert response.status_code == 200
    assert response.json()["setup"]["commit_message"] == "Add permission aware frontend action guards"

    download = client.get("/setup/guide/download")
    assert download.status_code == 200
    assert "Fresh Clone Setup Guide" in download.text
