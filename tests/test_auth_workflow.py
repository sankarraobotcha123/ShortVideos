from fastapi.testclient import TestClient

from app.core.config import settings
from app.db.session import init_db
from app.main import app


def test_default_admin_can_login_and_manage_users(tmp_path):
    settings.database_path = tmp_path / "auth-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.default_admin_email = "admin@example.com"
    settings.default_admin_password = "ChangeMe123!"
    init_db()

    client = TestClient(app)

    status = client.get("/api/auth/status")
    assert status.status_code == 200
    assert status.json()["default_admin_email"] == "admin@example.com"

    login = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "ChangeMe123!"})
    assert login.status_code == 200
    body = login.json()
    assert body["access_token"]
    assert body["user"]["role"] == "super_admin"

    headers = {"Authorization": f"Bearer {body['access_token']}"}
    users = client.get("/api/auth/users", headers=headers)
    assert users.status_code == 200
    assert len(users.json()["users"]) == 1

    created = client.post(
        "/api/auth/users",
        json={
            "name": "Script Reviewer",
            "email": "reviewer@example.com",
            "password": "ChangeMe123!",
            "role": "script_reviewer",
            "active": True,
        },
        headers=headers,
    )
    assert created.status_code == 200
    assert created.json()["user"]["role"] == "script_reviewer"


def test_user_management_requires_admin_token(tmp_path):
    settings.database_path = tmp_path / "auth-required-test.db"
    settings.export_dir = tmp_path / "exports"
    init_db()

    client = TestClient(app)
    unauthorized = client.get("/api/auth/users")
    assert unauthorized.status_code == 401


def test_strict_permission_enforcement_blocks_and_allows_creator_actions(tmp_path):
    settings.database_path = tmp_path / "strict-permission-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.auth_required = True
    settings.default_admin_email = "admin@example.com"
    settings.default_admin_password = "ChangeMe123!"
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

    try:
        blocked = client.post("/api/content/generate", json=payload)
        assert blocked.status_code == 401

        login = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "ChangeMe123!"})
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

        created = client.post("/api/content/generate", json=payload, headers=headers)
        assert created.status_code == 201
        package_id = created.json()["package"]["id"]

        users = client.get("/api/auth/users", headers=headers)
        assert users.status_code == 200

        reviewer = client.post(
            "/api/auth/users",
            json={
                "name": "Reviewer",
                "email": "reviewer@example.com",
                "password": "ChangeMe123!",
                "role": "script_reviewer",
                "active": True,
            },
            headers=headers,
        )
        assert reviewer.status_code == 200

        reviewer_login = client.post("/api/auth/login", json={"email": "reviewer@example.com", "password": "ChangeMe123!"})
        reviewer_headers = {"Authorization": f"Bearer {reviewer_login.json()['access_token']}"}

        denied_create = client.post("/api/content/generate", json=payload, headers=reviewer_headers)
        assert denied_create.status_code == 403

        allowed_review = client.patch(
            f"/api/content/{package_id}/review",
            json={
                "review_status": "approved",
                "script_text": created.json()["package"]["script_text"],
                "reviewer_notes": "Reviewer approved.",
            },
            headers=reviewer_headers,
        )
        assert allowed_review.status_code == 200
    finally:
        settings.auth_required = False


def test_auth_hardening_and_password_rotation(tmp_path):
    settings.database_path = tmp_path / "auth-hardening-test.db"
    settings.export_dir = tmp_path / "exports"
    settings.default_admin_email = "admin@example.com"
    settings.default_admin_password = "ChangeMe123!"
    settings.auth_required = False
    init_db()

    client = TestClient(app)
    blocked = client.get("/api/auth/hardening")
    assert blocked.status_code == 401

    login = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "ChangeMe123!"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    report = client.get("/api/auth/hardening", headers=headers)
    assert report.status_code == 200
    assert "checklist" in report.json()
    assert report.json()["active_sessions"] >= 1

    cleanup = client.post("/api/auth/sessions/cleanup", headers=headers)
    assert cleanup.status_code == 200
    assert "revoked_expired_sessions" in cleanup.json()

    changed = client.post(
        "/api/auth/change-password",
        json={"current_password": "ChangeMe123!", "new_password": "BetterPass123"},
        headers=headers,
    )
    assert changed.status_code == 200

    old_token_me = client.get("/api/auth/me", headers=headers)
    assert old_token_me.status_code == 200
    assert old_token_me.json()["authenticated"] is False

    old_password = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "ChangeMe123!"})
    assert old_password.status_code == 401

    new_password = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "BetterPass123"})
    assert new_password.status_code == 200
