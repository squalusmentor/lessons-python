"""Слой СЕРВИСА.

Сервис — это работа с данными: «достань пользователя», «сохрани пользователя».
Здесь живёт всё, что в реальном проекте ходило бы в БД. Сервис оперирует
МОДЕЛЯМИ (models/), а не схемами и не HTTP-объектами — он ничего не знает про
запросы и ответы.

Функции объявлены `async def` намеренно: в боевом коде внутри был бы
`await session.get(...)` к асинхронному драйверу БД. У нас данные статические,
поэтому await'ить нечего — но стиль сохраняем, чтобы переход на реальную БД был
бесшовным (см. теорию про event loop в readme).
"""

from source.models.user import User, FAKE_USERS


async def list_users() -> list[User]:
    """Вернуть всех пользователей."""
    return FAKE_USERS


async def get_user_by_id(user_id: int) -> User | None:
    """Найти пользователя по id, либо None, если такого нет."""
    for user in FAKE_USERS:
        if user.id == user_id:
            return user
    return None


async def create_user(first_name: str, last_name: str, email: str) -> User:
    """«Создать» пользователя: собрать доменную модель с новым (фейковым) id.

    В память ничего не пишем — просто возвращаем готовый объект.
    """
    new_id = max((user.id for user in FAKE_USERS), default=0) + 1
    return User(id=new_id, first_name=first_name, last_name=last_name, email=email)
