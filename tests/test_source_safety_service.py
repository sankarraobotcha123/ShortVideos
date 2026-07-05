from app.services.content_generator import ContentInput
from app.services.generation_orchestrator import generate_content_package_with_fallbacks
from app.services.source_safety_service import generate_source_safety_review


def test_source_safety_review_flags_copied_or_high_similarity(tmp_path):
    inp = ContentInput(
        board_source="Self-written",
        class_level="Class 7",
        subject="Science",
        topic="Why are leaves green?",
        audience="School students",
        language="English",
        duration_seconds=60,
        output_type="Short",
        tone="Curious",
        source_notes="Leaves contain chlorophyll. Chlorophyll reflects green light, so leaves look green.",
        source_name="Self notes",
        source_license_type="Original",
        copied_text_used=True,
        transformation_notes="Copied sample for testing risk detection.",
    )
    package = generate_content_package_with_fallbacks(inp)
    package.update({
        "id": 1,
        "source_notes": inp.source_notes,
        "source_name": inp.source_name,
        "source_license_type": inp.source_license_type,
        "copied_text_used": True,
        "transformation_notes": inp.transformation_notes,
    })
    review = generate_source_safety_review(package)
    assert review["risk_level"] == "high"
    assert review["status"] == "needs_rewrite"
    assert "Do not publish" in review["recommendation"]
    assert review["file_name"].endswith("source-safety-review.md")
