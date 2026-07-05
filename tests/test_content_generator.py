from app.services.content_generator import ContentInput, generate_content_package


def test_generate_content_package_has_required_outputs():
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
    package = generate_content_package(inp)
    assert package["hook"]
    assert package["script_text"]
    assert package["storyboard_markdown"].startswith("# Storyboard")
    assert "-->" in package["subtitle_srt"]
    assert package["trust_score"] >= 80
