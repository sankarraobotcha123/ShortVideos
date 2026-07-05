from app.services.provider_setup_service import build_provider_setup_guide


def test_provider_setup_guide_contains_profiles_and_fallback():
    guide = build_provider_setup_guide()
    assert guide["summary"]["commit_message"] == "Add real provider adapter setup guide"
    assert any(profile["key"] == "laptop_safe" for profile in guide["env_profiles"])
    assert any(profile["key"] == "ollama_desktop" for profile in guide["env_profiles"])
    assert "USE_OLLAMA=false" in guide["guide_markdown"]
    assert "template" in guide["guide_markdown"]
    assert "git status" in guide["git_commands"]


def test_provider_setup_guide_env_checks_shape():
    guide = build_provider_setup_guide()
    keys = {item["key"] for item in guide["env_checks"]}
    assert "AI_PROVIDER_CHAIN" in keys
    assert "USE_HOSTED_LLM" in keys
    assert "HOSTED_LLM_API_KEY" in keys
    assert guide["current_status"]
