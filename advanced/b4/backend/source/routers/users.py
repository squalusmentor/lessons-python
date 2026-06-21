from fastapi import APIRouter, Request, Response, HTTPException

from source.schemas.user import UserResponse, UserUpdateRequest
import source.handlers.users as users_handler

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, request: Request):
    result = await users_handler.get_user(user_id, request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, body: UserUpdateRequest, request: Request):
    result = await users_handler.update_user(user_id, body, request)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result


@router.delete("/{user_id}")
async def delete_user(user_id: int, request: Request, response: Response):
    result = await users_handler.delete_user(user_id, request, response)
    if result is False:
        raise HTTPException(status_code=500, detail="Unexpected error")
    return result
