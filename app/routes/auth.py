from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.core.config import settings
from app.services.auth_service import (
    ROLE_PERMISSIONS,
    auth_status,
    authenticate_user,
    create_session,
    create_user,
    current_user_optional,
    current_user_required,
    list_users,
    require_role,
    revoke_session,
    update_user,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1)


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str
    password: str = Field(min_length=8, max_length=200)
    role: str = "content_admin"
    active: bool = True


class UpdateUserRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    role: str | None = None
    active: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=200)


@router.get("/status")
def api_auth_status() -> dict[str, Any]:
    return auth_status()


@router.post("/login")
def api_login(payload: LoginRequest, response: Response) -> dict[str, Any]:
    user = authenticate_user(payload.email, payload.password)
    session = create_session(int(user["id"]))
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=session["access_token"],
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=settings.auth_token_ttl_hours * 60 * 60,
    )
    return {**session, "user": user}


@router.post("/logout")
def api_logout(
    request: Request,
    response: Response,
    user: dict[str, Any] | None = Depends(current_user_optional),
) -> dict[str, Any]:
    auth_header = request.headers.get("authorization", "")
    token = ""
    if auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
    token = token or request.cookies.get(settings.auth_cookie_name, "")
    if token:
        revoke_session(token)
    response.delete_cookie(settings.auth_cookie_name)
    return {"logged_out": True, "had_user": user is not None}


@router.get("/me")
def api_me(user: dict[str, Any] | None = Depends(current_user_optional)) -> dict[str, Any]:
    return {"user": user, "authenticated": user is not None}


@router.get("/roles")
def api_roles() -> dict[str, Any]:
    return {"roles": [{"role": role, "permissions": sorted(perms)} for role, perms in ROLE_PERMISSIONS.items()]}


@router.get("/users")
def api_list_users(_: dict[str, Any] = Depends(require_role("super_admin"))) -> dict[str, Any]:
    return {"users": list_users()}


@router.post("/users")
def api_create_user(
    payload: CreateUserRequest,
    _: dict[str, Any] = Depends(require_role("super_admin")),
) -> dict[str, Any]:
    user = create_user(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        role=payload.role,
        active=payload.active,
    )
    return {"user": user}


@router.patch("/users/{user_id}")
def api_update_user(
    user_id: int,
    payload: UpdateUserRequest,
    current_user: dict[str, Any] = Depends(require_role("super_admin")),
) -> dict[str, Any]:
    if current_user["id"] == user_id and payload.active is False:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account")
    user = update_user(
        user_id,
        name=payload.name,
        role=payload.role,
        active=payload.active,
        password=payload.password,
    )
    return {"user": user}
