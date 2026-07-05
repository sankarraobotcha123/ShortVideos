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
        "content:view",
        "content:create",
        "content:edit",
        "content:review",
        "content:publish",
        "assets:manage",
        "templates:manage",
        "analytics:view",
        "analytics:manage",
        "calendar:manage",
        "source_safety:review",
        "trust_score:review",
        "thumbnail:generate",
        "video:generate",
        "audio:generate",
        "learning_outputs:generate",
        "multilingual:manage",
    },
    "script_reviewer": {"content:view", "content:review", "source_safety:review", "trust_score:review", "analytics:view"},
    "video_editor": {"content:view", "content:edit", "assets:manage", "video:generate", "audio:generate", "thumbnail:generate"},
    "publisher": {"content:view", "content:publish", "calendar:manage", "analytics:view", "analytics:manage"},
    "viewer": {"content:view"},
}

DEFAULT_ROLE = "content_admin"
PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 120_000
bearer_scheme = HTTPBearer(auto_error=False)


def validate_password_strength(password: str) -> None:
    """MVP production guardrail for user-created passwords.

    This is intentionally simple and local-friendly: long enough, contains
    upper/lower/numeric characters, and rejects the documented sample password
    when strict auth is enabled.
    """
    if not password or len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.islower() for char in password):
        raise ValueError("Password must include at least one lowercase letter")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must include at least one uppercase letter")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must include at least one number")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_timestamp(dt: datetime | None = None) -> str:
    return (dt or utc_now()).replace(microsecond=0).isoformat()


def hash_password(password: str, salt: str | None = None) -> str:
    validate_password_strength(password)
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


def cleanup_expired_sessions(conn=None) -> int:
    """Revoke expired sessions and return how many rows were changed."""
    now = utc_timestamp()
    if conn is not None:
        before = conn.total_changes
        conn.execute(
            """
            UPDATE auth_sessions
               SET revoked_at = CURRENT_TIMESTAMP
             WHERE (revoked_at IS NULL OR revoked_at = '')
               AND expires_at <= ?
            """,
            (now,),
        )
        return conn.total_changes - before
    with db_session() as local_conn:
        return cleanup_expired_sessions(local_conn)


def enforce_session_limit(conn, user_id: int) -> int:
    """Keep only the newest N active sessions for a user."""
    max_sessions = max(int(settings.auth_max_active_sessions_per_user or 1), 1)
    rows = conn.execute(
        """
        SELECT id
          FROM auth_sessions
         WHERE user_id = ?
           AND (revoked_at IS NULL OR revoked_at = '')
           AND expires_at > ?
         ORDER BY created_at DESC, id DESC
        """,
        (user_id, utc_timestamp()),
    ).fetchall()
    stale_ids = [row["id"] for row in rows[max_sessions:]]
    if stale_ids:
        placeholders = ",".join("?" for _ in stale_ids)
        conn.execute(
            f"UPDATE auth_sessions SET revoked_at = CURRENT_TIMESTAMP WHERE id IN ({placeholders})",
            stale_ids,
        )
    return len(stale_ids)


def create_session(user_id: int) -> dict[str, Any]:
    token = secrets.token_urlsafe(40)
    expires_at = utc_timestamp(utc_now() + timedelta(hours=settings.auth_token_ttl_hours))
    with db_session() as conn:
        cleanup_expired_sessions(conn)
        conn.execute(
            """
            INSERT INTO auth_sessions (user_id, token, expires_at)
            VALUES (?, ?, ?)
            """,
            (user_id, token, expires_at),
        )
        enforce_session_limit(conn, user_id)
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


def _local_mvp_user(permission: str | None = None) -> dict[str, Any]:
    """Synthetic user used only when AUTH_REQUIRED=false.

    This keeps local solo development unblocked while letting the same route
    code become strict by setting AUTH_REQUIRED=true in `.env`.
    """
    permissions = {"*"} if permission else {"content:view"}
    return {
        "id": 0,
        "name": "Local MVP Developer",
        "email": "local-mvp@example.local",
        "role": "local_mvp",
        "active": True,
        "permissions": sorted(permissions),
        "auth_enforced": False,
    }


def require_role(*roles: str):
    def dependency(user: dict[str, Any] | None = Depends(current_user_optional)) -> dict[str, Any]:
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission for this action")
        return user

    return dependency


def require_permission(permission: str):
    def dependency(user: dict[str, Any] | None = Depends(current_user_optional)) -> dict[str, Any]:
        if user is None and not settings.auth_required:
            return _local_mvp_user(permission)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
        if not role_has_permission(user.get("role", "viewer"), permission):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing permission: {permission}")
        return user

    return dependency


def permission_matrix() -> list[dict[str, Any]]:
    return [
        {"role": role, "permissions": sorted(perms)}
        for role, perms in ROLE_PERMISSIONS.items()
    ]


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




def change_password(user_id: int, current_password: str, new_password: str) -> None:
    with db_session() as conn:
        row = conn.execute("SELECT * FROM user_accounts WHERE id = ?", (user_id,)).fetchone()
        if row is None or not verify_password(current_password, row["password_hash"]):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
        conn.execute(
            "UPDATE user_accounts SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (hash_password(new_password), user_id),
        )
        conn.execute(
            "UPDATE auth_sessions SET revoked_at = CURRENT_TIMESTAMP WHERE user_id = ? AND (revoked_at IS NULL OR revoked_at = '')",
            (user_id,),
        )


def auth_hardening_report() -> dict[str, Any]:
    with db_session() as conn:
        cleanup_expired_sessions(conn)
        active_sessions = conn.execute(
            """
            SELECT COUNT(*) AS count
              FROM auth_sessions
             WHERE (revoked_at IS NULL OR revoked_at = '')
               AND expires_at > ?
            """,
            (utc_timestamp(),),
        ).fetchone()["count"]
        expired_or_revoked = conn.execute(
            """
            SELECT COUNT(*) AS count
              FROM auth_sessions
             WHERE revoked_at IS NOT NULL AND revoked_at != ''
            """
        ).fetchone()["count"]
        users_total = conn.execute("SELECT COUNT(*) AS count FROM user_accounts").fetchone()["count"]
        inactive_users = conn.execute("SELECT COUNT(*) AS count FROM user_accounts WHERE active = 0").fetchone()["count"]

    warnings: list[str] = []
    recommendations: list[str] = []
    if not settings.auth_required:
        warnings.append("AUTH_REQUIRED is false; local MVP mode is permissive.")
        recommendations.append("Set AUTH_REQUIRED=true before testing production-style review and publishing controls.")
    if settings.default_admin_password == "ChangeMe123!":
        warnings.append("Default admin password still uses the sample value from the documentation.")
        recommendations.append("Change DEFAULT_ADMIN_PASSWORD in .env, recreate the local DB, or update the admin password from the UI.")
    if settings.auth_required and not settings.auth_cookie_secure:
        warnings.append("AUTH_COOKIE_SECURE is false while strict auth is enabled.")
        recommendations.append("Set AUTH_COOKIE_SECURE=true when serving over HTTPS.")
    if settings.auth_token_ttl_hours > 168:
        warnings.append("Auth token TTL is longer than 7 days.")
        recommendations.append("Use a shorter AUTH_TOKEN_TTL_HOURS value for production-like environments.")

    checklist = [
        {"item": "Strict auth enabled", "passed": bool(settings.auth_required)},
        {"item": "Default password changed", "passed": settings.default_admin_password != "ChangeMe123!"},
        {"item": "Session limit configured", "passed": settings.auth_max_active_sessions_per_user <= 10},
        {"item": "Cookie SameSite configured", "passed": settings.auth_cookie_samesite in {"lax", "strict", "none"}},
        {"item": "Secure cookie ready for HTTPS", "passed": bool(settings.auth_cookie_secure) or not settings.auth_required},
    ]
    return {
        "auth_required": settings.auth_required,
        "cookie_secure": settings.auth_cookie_secure,
        "cookie_samesite": settings.auth_cookie_samesite,
        "token_ttl_hours": settings.auth_token_ttl_hours,
        "max_active_sessions_per_user": settings.auth_max_active_sessions_per_user,
        "active_sessions": active_sessions,
        "expired_or_revoked_sessions": expired_or_revoked,
        "users_total": users_total,
        "inactive_users": inactive_users,
        "warnings": warnings,
        "recommendations": recommendations,
        "checklist": checklist,
    }


def revoke_expired_sessions() -> dict[str, Any]:
    count = cleanup_expired_sessions()
    return {"revoked_expired_sessions": count}

def auth_status() -> dict[str, Any]:
    return {
        "auth_required": settings.auth_required,
        "cookie_name": settings.auth_cookie_name,
        "token_ttl_hours": settings.auth_token_ttl_hours,
        "cookie_secure": settings.auth_cookie_secure,
        "cookie_samesite": settings.auth_cookie_samesite,
        "max_active_sessions_per_user": settings.auth_max_active_sessions_per_user,
        "roles": permission_matrix(),
        "default_admin_email": settings.default_admin_email,
        "note": "Default admin is created only when the database has no users.",
    }
