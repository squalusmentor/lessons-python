"""Слой ХЕНДЛЕРОВ (бизнес-логика).

Хендлер — посредник между роутером и сервисом. Он:
- принимает уже провалидированные данные от роутера;
- вызывает нужные функции сервиса;
- принимает решения и бросает HTTP-ошибки (404, 403, ...), если что-то не так.

Хендлер ничего не знает про URL и методы (это забота роутера) и не лезет напрямую
в данные (это забота сервиса). Поэтому его легко тестировать отдельно.
"""

from fastapi import HTTPException

from source.models.user import User
from source.schemas.user import UserCreate
import source.services.users as users_service


async def list_users() -> list[User]:
    return await users_service.list_users()


async def get_user(user_id: int) -> User:
    user = await users_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_user(body: UserCreate) -> User:
    return await users_service.create_user(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
    )
