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
