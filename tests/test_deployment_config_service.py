from app.services.deployment_config_service import build_deployment_config_guide


def test_deployment_config_guide_contains_packaging_workflow():
    guide = build_deployment_config_guide()
    assert guide["summary"]["commit_message"] == "Add deployment packaging and production configuration guide"
    assert "python scripts/build_release_package.py" in guide["packaging_commands"]
    assert "AUTH_REQUIRED=true" in guide["guide_markdown"]
    assert "Deployment Packaging and Production Configuration Guide" in guide["guide_markdown"]
    assert any(item["key"] == "AUTH_REQUIRED" for item in guide["production_env_checks"])
    assert "dist_release/" in guide["protected_paths"]


def test_deployment_config_guide_has_deployment_phases():
    guide = build_deployment_config_guide()
    phases = {item["title"] for item in guide["deployment_steps"]}
    assert "Prepare production environment" in phases
    assert "Build frontend" in phases
    assert "Run backend" in phases
