from fastapi import Request, Response, HTTPException
from sqlalchemy import select

from source.db_connect import async_session
from source.models.user import User
from source.schemas.auth import SignUpRequest, SignInRequest
from source.services.decorators import handle_errors_async
from source.services.scripts import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token
)


def _set_auth_cookies(response: Response, user_id: int):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax")
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        samesite="lax",
        path="/auth/refresh"
    )


def _delete_auth_cookies(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token", path="/auth/refresh")


@handle_errors_async
async def sign_up(body: SignUpRequest, response: Response):
    if body.password != body.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    async with async_session() as session:
        existing = await session.scalar(
            select(User).where(User.email == body.email)
        )
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

        user = User(
            first_name=body.first_name,
            last_name=body.last_name,
            middle_name=body.middle_name,
            email=body.email,
            password_hash=hash_password(body.password),
        )
        session.add(user)
        await session.commit()

    _set_auth_cookies(response, user.id)
    return {"message": "Registered successfully"}


@handle_errors_async
async def sign_in(body: SignInRequest, response: Response):
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.email == body.email)
        )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    _set_auth_cookies(response, user.id)
    return {"message": "Signed in successfully"}


@handle_errors_async
async def sign_out(response: Response):
    _delete_auth_cookies(response)
    return {"message": "Signed out successfully"}


@handle_errors_async
async def refresh(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    user_id = decode_token(token, token_type="refresh")
    if user_id is False:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(user_id)
    response.set_cookie("access_token", access_token, httponly=True, samesite="lax")
    return {"message": "Token refreshed"}
