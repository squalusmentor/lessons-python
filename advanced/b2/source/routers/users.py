"""Слой РОУТЕРОВ.

Роутер отвечает ровно за одно: какой `метод + путь` -> какая функция-хендлер.
Здесь же объявляются схемы запроса/ответа (`response_model`, тип тела). Никакой
логики — роутер только разбирает HTTP и делегирует хендлеру.

APIRouter — это «мини-приложение»: группа роутов одного ресурса, которую main.py
подключает целиком через include_router(prefix="/users").
"""

from fastapi import APIRouter

from source.schemas.user import UserCreate, UserResponse
import source.handlers.users as users_handler

router = APIRouter()


@router.get("", response_model=list[UserResponse])
async def list_users():
    """GET /users — список пользователей (отдаём статические модели)."""
    return await users_handler.list_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """GET /users/{user_id} — один пользователь, либо 404."""
    return await users_handler.get_user(user_id)


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(body: UserCreate):
    """POST /users — принимаем модель из тела, возвращаем созданную модель."""
    return await users_handler.create_user(body)
