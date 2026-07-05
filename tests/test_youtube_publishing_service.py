from app.services.youtube_publishing_service import build_youtube_publishing_checklist


def test_youtube_publishing_checklist_contains_manual_workflow():
    checklist = build_youtube_publishing_checklist()
    assert checklist["summary"]["commit_message"] == "Add YouTube publishing checklist workflow"
    assert checklist["summary"]["manual_upload_first"] is True
    assert any(phase["key"] == "youtube_studio_upload" for phase in checklist["manual_publishing_phases"])
    assert "YOUTUBE_API_ENABLED=false" in checklist["guide_markdown"]
    assert "No automatic YouTube upload is implemented" in checklist["guide_markdown"]
    assert "git status" in checklist["git_commands"]


def test_youtube_publishing_env_checks_shape():
    checklist = build_youtube_publishing_checklist()
    keys = {item["key"] for item in checklist["env_checks"]}
    assert "YOUTUBE_API_ENABLED" in keys
    assert "YOUTUBE_CLIENT_SECRETS_FILE" in keys
    assert "YOUTUBE_TOKEN_FILE" in keys
    assert checklist["api_safety_boundaries"]
