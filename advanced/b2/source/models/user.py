"""Слой МОДЕЛЕЙ.

Модель — это доменная сущность приложения, обычный Python-объект, который ничего
не знает ни про HTTP, ни про pydantic. В настоящем проекте здесь была бы ORM-модель
(строка таблицы в БД). У нас БД нет, поэтому модель — простой dataclass, а вместо
таблицы — заранее заданный список объектов в памяти («статические модели»).
"""

from dataclasses import dataclass


@dataclass
class User:
    """Доменная модель пользователя."""
    id: int
    first_name: str
    last_name: str
    email: str


# Вместо базы данных — фиксированные объекты в памяти.
FAKE_USERS: list[User] = [
    User(id=1, first_name="Иван", last_name="Петров", email="ivan@example.com"),
    User(id=2, first_name="Мария", last_name="Сидорова", email="maria@example.com"),
    User(id=3, first_name="Олег", last_name="Кузнецов", email="oleg@example.com"),
]
