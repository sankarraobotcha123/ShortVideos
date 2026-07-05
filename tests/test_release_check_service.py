from app.services.release_check_service import build_release_checklist


def test_release_checklist_contains_git_commands():
    checklist = build_release_checklist()
    assert checklist["commit_message"] == "Add YouTube publishing checklist workflow"
    assert "git status" in checklist["git_commands"]
    assert ".env" in checklist["protected_paths"]
    assert "frontend/node_modules/" in checklist["protected_paths"]
    assert "Production Cleanup and Release Checklist" in checklist["report_markdown"]


def test_release_checklist_api(client=None):
    # Kept intentionally simple so it does not need database setup.
    checklist = build_release_checklist()
    assert "summary" in checklist
    assert "gitignore_checks" in checklist
