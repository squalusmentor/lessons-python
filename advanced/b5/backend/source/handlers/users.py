from fastapi import Request, Response, HTTPException

from source.db_connect import async_session
from source.models.user import User
from source.schemas.user import UserUpdateRequest
from source.services.decorators import handle_errors_async
from source.services.scripts import decode_token, hash_password


def _get_current_user_id(request: Request) -> int:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_token(token)
    if user_id is False:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id


@handle_errors_async
async def get_user(user_id: int, request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if current_user_id != user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Forbidden")

        target_user = await session.get(User, user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

    return target_user


@handle_errors_async
async def update_user(user_id: int, body: UserUpdateRequest, request: Request):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if current_user_id != user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Forbidden")

        target_user = await session.get(User, user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

        if body.first_name is not None:
            target_user.first_name = body.first_name
        if body.last_name is not None:
            target_user.last_name = body.last_name
        if body.middle_name is not None:
            target_user.middle_name = body.middle_name
        if body.email is not None:
            target_user.email = body.email
        if body.password is not None:
            target_user.password_hash = hash_password(body.password)
        if body.is_active is not None:
            target_user.is_active = body.is_active

        await session.commit()
        await session.refresh(target_user)

    return target_user


@handle_errors_async
async def delete_user(user_id: int, request: Request, response: Response):
    current_user_id = _get_current_user_id(request)

    async with async_session() as session:
        current_user = await session.get(User, current_user_id)
        if not current_user or not current_user.is_active:
            raise HTTPException(status_code=401, detail="Not authenticated")

        if current_user_id != user_id and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Forbidden")

        target_user = await session.get(User, user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")

        target_user.is_active = False
        await session.commit()

    if current_user_id == user_id:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token", path="/auth/refresh")

    return {"message": "User deactivated"}
