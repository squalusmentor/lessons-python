"""Слой СХЕМ (pydantic).

Схема описывает форму данных НА ГРАНИЦЕ HTTP: что приходит в теле запроса и что
уходит в теле ответа. Это «контракт» API. FastAPI по схемам сам валидирует вход,
сериализует выход и строит документацию.

Важно не путать схему и модель:
- модель (models/) — внутренняя сущность приложения;
- схема  (schemas/) — то, что видит клиент снаружи.
Их разделяют, чтобы наружу не утекали лишние/секретные поля.
"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Схема ВХОДА: тело POST-запроса на создание пользователя."""
    first_name: str
    last_name: str
    email: EmailStr           # EmailStr проверит, что строка похожа на email


class UserResponse(BaseModel):
    """Схема ВЫХОДА: то, что сервер отдаёт наружу."""
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    # from_attributes=True позволяет собрать схему прямо из объекта-модели
    # (читать поля через атрибуты user.id, user.email, ...), а не из словаря.
    model_config = {"from_attributes": True}
