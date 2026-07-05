from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.db.session import db_session


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "super_admin": {"*"},
    "content_admin": {
        "content:create",
        "content:edit",
        "content:review",
        "content:publish",
        "assets:manage",
        "templates:manage",
        "analytics:view",
    },
    "script_reviewer": {"content:review", "source_safety:review", "trust_score:review", "analytics:view"},
    "video_editor": {"content:edit", "assets:manage", "video:generate", "thumbnail:generate"},
    "publisher": {"content:publish", "calendar:manage", "analytics:view"},
    "viewer": {"content:view"},
}

DEFAULT_ROLE = "content_admin"
PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 120_000
bearer_scheme = HTTPBearer(auto_error=False)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_timestamp(dt: datetime | None = None) -> str:
    return (dt or utc_now()).replace(microsecond=0).isoformat()


def hash_password(password: str, salt: str | None = None) -> str:
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    ).hex()
    return f"{PASSWORD_ALGORITHM}${PASSWORD_ITERATIONS}${salt}${digest}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt, digest = stored_hash.split("$", 3)
        if algorithm != PASSWORD_ALGORITHM:
            return False
        iterations = int(iterations_text)
        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        ).hex()
        return hmac.compare_digest(candidate, digest)
    except Exception:
        return False


def serialize_user(row: Any) -> dict[str, Any]:
    user = dict(row)
    user.pop("password_hash", None)
    user["active"] = bool(user.get("active"))
    user["permissions"] = sorted(ROLE_PERMISSIONS.get(user.get("role", "viewer"), set()))
    return user


def role_has_permission(role: str, permission: str) -> bool:
    permissions = ROLE_PERMISSIONS.get(role, set())
    return "*" in permissions or permission in permissions


def bootstrap_default_admin(conn) -> dict[str, Any] | None:
    """Create a local admin if no users exist yet.

    The password comes from `.env` / `.env.example`. Existing users are never
    overwritten, so changing the env value will not silently reset production data.
    """
    count = conn.execute("SELECT COUNT(*) AS count FROM user_accounts").fetchone()["count"]
    if count:
        return None

    password_hash = hash_password(settings.default_admin_password)
    cursor = conn.execute(
        """
        INSERT INTO user_accounts (name, email, password_hash, role, active)
        VALUES (?, ?, ?, 'super_admin', 1)
        """,
        (settings.default_admin_name, settings.default_admin_email.lower().strip(), password_hash),
    )
    row = conn.execute("SELECT * FROM user_accounts WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return serialize_user(row)


def authenticate_user(email: str, password: str) -> dict[str, Any]:
    normalized_email = email.lower().strip()
    with db_session() as conn:
        row = conn.execute("SELECT * FROM user_accounts WHERE email = ?", (normalized_email,)).fetchone()
        if row is None or not row["active"] or not verify_password(password, row["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        user = serialize_user(row)
        conn.execute("UPDATE user_accounts SET last_login_at = CURRENT_TIMESTAMP WHERE id = ?", (user["id"],))
        return user


def create_session(user_id: int) -> dict[str, Any]:
    token = secrets.token_urlsafe(40)
    expires_at = utc_timestamp(utc_now() + timedelta(hours=settings.auth_token_ttl_hours))
    with db_session() as conn:
        conn.execute(
            """
            INSERT INTO auth_sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
            """,
            (user_id, token, expires_at),
        )
    return {"access_token": token, "token_type": "bearer", "expires_at": expires_at}


def revoke_session(token: str) -> None:
    with db_session() as conn:
        conn.execute("UPDATE auth_sessions SET revoked_at = CURRENT_TIMESTAMP WHERE token = ?", (token,))


def _token_from_request(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None,
) -> str | None:
    if credentials and credentials.scheme.lower() == "bearer" and credentials.credentials:
        return credentials.credentials
    cookie_token = request.cookies.get(settings.auth_cookie_name)
    return cookie_token or None


def get_user_by_token(token: str | None) -> dict[str, Any] | None:
    if not token:
        return None
    with db_session() as conn:
        row = conn.execute(
            """
            SELECT u.*
            FROM auth_sessions s
            JOIN user_accounts u ON u.id = s.user_id
            WHERE s.token = ?
              AND (s.revoked_at IS NULL OR s.revoked_at = '')
              AND s.expires_at > ?
              AND u.active = 1
            """,
            (token, utc_timestamp()),
        ).fetchone()
        return serialize_user(row) if row else None


def current_user_optional(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any] | None:
    token = _token_from_request(request, credentials)
    return get_user_by_token(token)


def current_user_required(
    user: dict[str, Any] | None = Depends(current_user_optional),
) -> dict[str, Any]:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
    return user


def require_role(*roles: str):
    def dependency(user: dict[str, Any] = Depends(current_user_required)) -> dict[str, Any]:
        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission for this action")
        return user

    return dependency


def require_permission(permission: str):
    def dependency(user: dict[str, Any] = Depends(current_user_required)) -> dict[str, Any]:
        if not role_has_permission(user.get("role", "viewer"), permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission for this action")
        return user

    return dependency


def list_users() -> list[dict[str, Any]]:
    with db_session() as conn:
        rows = conn.execute("SELECT * FROM user_accounts ORDER BY created_at DESC, id DESC").fetchall()
        return [serialize_user(row) for row in rows]


def create_user(*, name: str, email: str, password: str, role: str, active: bool = True) -> dict[str, Any]:
    if role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=400, detail="Unsupported role")
    normalized_email = email.lower().strip()
    try:
        password_hash = hash_password(password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    with db_session() as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO user_accounts (name, email, password_hash, role, active)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name.strip(), normalized_email, password_hash, role, int(active)),
            )
        except Exception as exc:
            if "UNIQUE" in str(exc).upper():
                raise HTTPException(status_code=409, detail="A user with this email already exists") from exc
            raise
        row = conn.execute("SELECT * FROM user_accounts WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return serialize_user(row)


def update_user(
    user_id: int,
    *,
    name: str | None = None,
    role: str | None = None,
    active: bool | None = None,
    password: str | None = None,
) -> dict[str, Any]:
    if role is not None and role not in ROLE_PERMISSIONS:
        raise HTTPException(status_code=400, detail="Unsupported role")
    fields: list[str] = []
    values: list[Any] = []
    if name is not None:
        fields.append("name = ?")
        values.append(name.strip())
    if role is not None:
        fields.append("role = ?")
        values.append(role)
    if active is not None:
        fields.append("active = ?")
        values.append(int(active))
    if password:
        try:
            password_hash = hash_password(password)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        fields.append("password_hash = ?")
        values.append(password_hash)
    if not fields:
        with db_session() as conn:
            row = conn.execute("SELECT * FROM user_accounts WHERE id = ?", (user_id,)).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="User not found")
            return serialize_user(row)

    fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(user_id)
    with db_session() as conn:
        existing = conn.execute("SELECT id FROM user_accounts WHERE id = ?", (user_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="User not found")
        conn.execute(f"UPDATE user_accounts SET {', '.join(fields)} WHERE id = ?", values)
        row = conn.execute("SELECT * FROM user_accounts WHERE id = ?", (user_id,)).fetchone()
        return serialize_user(row)


def auth_status() -> dict[str, Any]:
    return {
        "auth_required": settings.auth_required,
        "cookie_name": settings.auth_cookie_name,
        "token_ttl_hours": settings.auth_token_ttl_hours,
        "roles": [
            {"role": role, "permissions": sorted(perms)}
            for role, perms in ROLE_PERMISSIONS.items()
        ],
        "default_admin_email": settings.default_admin_email,
        "note": "Default admin is created only when the database has no users.",
    }
