from app.services.content_generator import ContentInput
from app.services.generation_orchestrator import generate_content_package_with_fallbacks, provider_status


def test_fallback_generation_always_returns_package():
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
        source_notes="Leaves contain chlorophyll. Chlorophyll reflects green light.",
        source_name="Self notes",
        source_license_type="Original",
        transformation_notes="Original analogy and visual flow added.",
    )
    package = generate_content_package_with_fallbacks(inp)
    assert package["script_text"]
    assert package["provider_used"] in {"template", "ollama", "transformers"}
    assert "template" in package["provider_chain"]


def test_provider_status_contains_template():
    statuses = provider_status()
    template = next(item for item in statuses if item["name"] == "template")
    assert template["available"] is True
