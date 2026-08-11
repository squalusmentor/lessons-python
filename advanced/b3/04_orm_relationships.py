"""Блок 2 (продолжение). Связь один-ко-многим: User -> Articles.

Это модель из референс-проекта: у пользователя (users) много статей (articles),
каждая статья принадлежит одному автору. Связь держится на ВНЕШНЕМ КЛЮЧЕ
(ForeignKey): в articles есть столбец owner_id, указывающий на users.id.

Здесь намеренно ПРОСТО: никаких relationship() и selectinload. Связь между
таблицами читаем обычным JOIN'ом — той же идеей, что в сыром SQL (01, 02), только
запрос собираем через select().join(). Так видно механизм: чтобы соединить данные
двух таблиц, их джойнят по ключу.

    Есть и "продвинутый" способ: описать relationship() и ходить по связи как по
    атрибуту (user.articles). Он удобнее, но в async требует явной подгрузки
    (selectinload) и своих подводных камней. Это следующий уровень — не сейчас.
"""

import asyncio
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_PATH = Path(__file__).parent / "demo_rel.db"
SQLITE_URL = f"sqlite+aiosqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    # Вся связь — вот этот столбец. Внешний ключ owner_id ссылается на users.id.
    # ondelete="CASCADE": удалили пользователя -> его статьи удалятся автоматически.
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))


# Плоская Pydantic-схема: отдаём статью как есть, вместе с id её автора.
class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    owner_id: int


engine = create_async_engine(SQLITE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def demo4():
    print("== 04. Связь один-ко-многим: User -> Articles ==\n")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # --- Создаём авторов и их статьи ------------------------------------------
    async with async_session() as session:
        ivan = User(name="Иван")
        maria = User(name="Мария")
        session.add_all([ivan, maria])
        # flush отправляет INSERT'ы в БД внутри транзакции, и БД присваивает id.
        # После этого ivan.id и maria.id уже известны — их и ставим статьям.
        await session.flush()

        session.add_all([
            Article(title="Введение в asyncio", owner_id=ivan.id),
            Article(title="ORM за 10 минут", owner_id=ivan.id),
            Article(title="Postgres для начинающих", owner_id=maria.id),
        ])
        await session.commit()
        print("Создали 2 авторов и 3 статьи (owner_id проставлен вручную).\n")

    # --- Читаем связанные данные обычным JOIN ---------------------------------
    async with async_session() as session:
        # select с двумя таблицами + join по ключу. Результат — строки-кортежи
        # (имя автора, заголовок статьи), как в сыром SQL.
        result = await session.execute(
            select(User.name, Article.title)
            .join(Article, Article.owner_id == User.id)
            .order_by(User.name, Article.title)
        )
        print("Автор -> статья (через JOIN):")
        for name, title in result.all():
            print(f"  {name} -> {title}")

    # --- Тот же JOIN, но с фильтром: только статьи Ивана -----------------------
    async with async_session() as session:
        result = await session.execute(
            select(Article.title)
            .join(User, User.id == Article.owner_id)
            .where(User.name == "Иван")
        )
        print("\nСтатьи Ивана:", [row[0] for row in result.all()])

    # --- ORM-объекты + Pydantic (как в 03) ------------------------------------
    async with async_session() as session:
        # select(Article) без join вернёт сами объекты Article; owner_id — обычный
        # столбец, он уже загружен, за ним в БД повторно ходить не надо.
        articles = (await session.scalars(select(Article).order_by(Article.id))).all()
        print("\nСтатьи как объекты -> Pydantic:")
        for a in articles:
            print("  ", ArticleOut.model_validate(a).model_dump())

    await engine.dispose()
    print("\nИтог: связь один-ко-многим = внешний ключ owner_id; чтобы собрать")
    print("данные двух таблиц, соединяем их JOIN'ом по этому ключу.")


if __name__ == "__main__":
    asyncio.run(demo4())
