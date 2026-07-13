"""Блок 2. ORM: SQLAlchemy 2.0 (async) + Pydantic.

В 01-02 мы писали SQL руками и разбирали кортежи. ORM (Object-Relational Mapping)
переворачивает это: ТАБЛИЦА <-> КЛАСС, СТРОКА <-> ОБЪЕКТ. Ты работаешь с обычными
Python-объектами, а SQLAlchemy сам генерирует SQL под нужную БД.

Что берём на вооружение:
- create_async_engine  — асинхронный "движок": пул соединений + таймауты + драйвер;
- async_sessionmaker   — фабрика СЕССИЙ;
- DeclarativeBase      — базовый класс для моделей (стиль SQLAlchemy 2.0);
- Mapped / mapped_column — типизированное описание столбцов.

Здесь работаем на SQLite (файл, ничего поднимать не надо). Чтобы переехать на
Postgres, меняется РОВНО ОДНА строка — URL движка (см. POSTGRES_URL ниже). Весь
остальной код остаётся тем же — в этом главный смысл ORM.

Pydantic в паре с ORM ("ORM Pydantic"): ORM-модель — это то, как данные лежат в
БД (включая секреты вроде password_hash). Pydantic-схема — это то, что мы отдаём
наружу. Одна строка password_hash не попадает в схему -> физически не утечёт в
ответ. Ровно та же связка "модель vs схема", что в уроке B4, только модель теперь
настоящая, из БД.
"""

import asyncio
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_PATH = Path(__file__).parent / "demo_orm.db"

# URL движка = "драйвер + адрес БД". Диалект и async-драйвер зашиты в схему URL:
SQLITE_URL = f"sqlite+aiosqlite:///{DB_PATH}"
# Чтобы переехать на Postgres — просто раскомментируй строку ниже и передай её в
# create_async_engine вместо SQLITE_URL. Больше НИЧЕГО менять не нужно:
POSTGRES_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


# --- Модель -------------------------------------------------------------------
class Base(DeclarativeBase):
    """Общий предок всех моделей. Хранит metadata — реестр всех таблиц."""


class User(Base):
    __tablename__ = "users"

    # Mapped[int] — тип поля в Python; mapped_column(...) — как столбец в БД.
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    # Секрет: лежит в БД, но в Pydantic-схему ниже мы его НЕ включаем.
    password_hash: Mapped[str] = mapped_column(String(255))
    # Mapped[str | None] -> столбец nullable (может быть NULL).
    bio: Mapped[str | None] = mapped_column(String(500), default=None)

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"


# --- Pydantic-схема (то, что отдаём наружу) -----------------------------------
class UserOut(BaseModel):
    # from_attributes=True разрешает собрать схему прямо из ORM-объекта
    # (читать user.id, user.email через атрибуты). Без него model_validate ждёт dict.
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    bio: str | None
    # password_hash здесь НЕТ -> в наружу он не попадёт, даже если есть в модели.


# --- Движок и фабрика сессий --------------------------------------------------
# echo=True печатал бы весь генерируемый SQL — полезно, чтобы увидеть, что делает
# ORM. Оставим False, чтобы вывод демо был чистым.
# connect_args пробрасывается драйверу: для asyncpg так задаётся таймаут коннекта:
#   create_async_engine(POSTGRES_URL, connect_args={"timeout": 5})
engine = create_async_engine(SQLITE_URL, echo=False)

# expire_on_commit=False — после commit объекты остаются "живыми": их поля можно
# читать без нового похода в БД. Без этого SQLAlchemy после commit пометил бы поля
# устаревшими и при первом же обращении полез бы за ними в базу (в async это ещё и
# требует await и может выстрелить ошибкой). Для веб-хендлеров это стандарт.
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def demo3():
    print("== 03. ORM: SQLAlchemy 2.0 async + Pydantic ==\n")

    # --- Создание таблиц ------------------------------------------------------
    # run_sync нужен потому, что create_all — синхронная операция; движок исполняет
    # её на своём соединении. drop_all в начале делает демо идемпотентным.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # --- CREATE: добавляем объекты --------------------------------------------
    # Сессия — "единица работы" (unit of work): копишь в ней изменения, а commit
    # отправляет их в БД одной транзакцией. async with сам закроет сессию.
    async with async_session() as session:
        session.add(User(name="Иван", email="ivan@example.com", password_hash="x1"))
        session.add_all([
            User(name="Мария", email="maria@example.com", password_hash="x2", bio="QA"),
            User(name="Олег", email="oleg@example.com", password_hash="x3"),
        ])
        # Пока commit не сделан, в БД ничего нет — всё копится в сессии.
        await session.commit()
        print("Добавили 3 пользователей одной транзакцией.\n")

    # --- READ: select() -------------------------------------------------------
    async with async_session() as session:
        # select(User) описывает запрос; execute его выполняет.
        result = await session.execute(select(User).order_by(User.id))
        # scalars() разворачивает строки-кортежи в сами объекты User.
        users = result.scalars().all()
        print("Все пользователи (объекты, а не кортежи!):")
        for u in users:
            print("  ", u)

        # Поиск по условию -> один объект или None.
        result = await session.execute(select(User).where(User.email == "maria@example.com"))
        maria = result.scalar_one_or_none()
        print("\nНашли по email:", maria)

        # get(Model, pk) — быстрый поиск по первичному ключу.
        user1 = await session.get(User, 1)
        print("get по id=1:", user1)

    # --- UPDATE: меняем атрибут, сессия сама видит изменение -------------------
    async with async_session() as session:
        user = await session.get(User, 1)
        user.name = "Иван Петров"        # просто присваиваем — unit of work заметит
        await session.commit()           # и на commit сгенерирует UPDATE
        print("\nПосле UPDATE:", await session.get(User, 1))

    # --- DELETE ---------------------------------------------------------------
    async with async_session() as session:
        oleg = await session.scalar(select(User).where(User.name == "Олег"))
        await session.delete(oleg)
        await session.commit()
        remaining = (await session.execute(select(User))).scalars().all()
        print("После DELETE осталось:", len(remaining), "пользователей")

    # --- Мост ORM -> Pydantic -------------------------------------------------
    async with async_session() as session:
        user = await session.get(User, 2)
        # model_validate собирает Pydantic-схему прямо из ORM-объекта.
        schema = UserOut.model_validate(user)
        print("\nORM-объект содержит password_hash:", user.password_hash)
        print("А Pydantic-схема наружу его НЕ отдаёт:")
        print("  ", schema.model_dump())      # password_hash отсутствует

    await engine.dispose()   # закрываем пул соединений движка
    print("\nИтог: ORM вернул готовые объекты User; Pydantic отфильтровал секреты.")


if __name__ == "__main__":
    asyncio.run(demo3())
