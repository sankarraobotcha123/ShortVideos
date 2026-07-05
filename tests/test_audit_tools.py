from pathlib import Path

from app.services.release_check_service import build_release_checklist


def test_audit_tools_are_in_release_checklist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "scripts" / "run_tests.py").exists()
    assert (root / "scripts" / "clean_local_artifacts.py").exists()
    assert (root / "docs" / "PROJECT_AUDIT_V34.md").exists()

    checklist = build_release_checklist(root)
    labels = {item["label"] for item in checklist["file_checks"]}
    assert "scripts/run_tests.py" in labels
    assert "scripts/clean_local_artifacts.py" in labels
    assert "docs/PROJECT_AUDIT_V34.md" in labels
    assert "python scripts/run_tests.py" in checklist["git_commands"]
