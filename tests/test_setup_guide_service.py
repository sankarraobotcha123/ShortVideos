from app.services.setup_guide_service import build_setup_guide


def test_setup_guide_contains_fresh_clone_commands():
    guide = build_setup_guide()
    assert guide["commit_message"] == "Add content production board workflow"
    assert "setup_windows.bat" in guide["guide_markdown"]
    assert "python scripts/setup_project.py --seed-demo" in guide["guide_markdown"]
    assert "git status" in guide["git_commands"]
    assert any(item["label"] == "scripts/setup_project.py" for item in guide["required_setup_files"])


def test_setup_guide_summary_shape():
    guide = build_setup_guide()
    assert "summary" in guide
    assert "setup_steps" in guide
    assert len(guide["setup_steps"]) >= 5
    assert "windows_setup_commands" in guide
