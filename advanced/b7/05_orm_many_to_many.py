"""Блок 2 (финал). Связь многие-ко-многим: Article <-> Tag.

Один-ко-многим (файл 04) держался на одном внешнем ключе. Многие-ко-многим так
не выразить: у статьи много тегов И у тега много статей. Нужна ТРЕТЬЯ таблица —
"ассоциативная" (junction table). Каждая её строка — это пара (article_id, tag_id),
то есть один факт "у этой статьи есть этот тег". Вся связь = набор таких пар.

Держим тот же простой стиль, что в 04: никаких relationship() и selectinload.
Связи в ассоциативную таблицу пишем явными строками, а читаем обычным JOIN'ом —
теперь по трём таблицам сразу (articles + article_tags + tags).

    "Продвинутый" способ — relationship(secondary=...), тогда работаешь со списком
    article.tags. Удобнее, но это следующий уровень; сейчас важно увидеть механизм.
"""

import asyncio
from pathlib import Path

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, ForeignKey, String, Table, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_PATH = Path(__file__).parent / "demo_m2m.db"
SQLITE_URL = f"sqlite+aiosqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


# --- Ассоциативная таблица: только две колонки-ключа, без своей модели ---------
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


engine = create_async_engine(SQLITE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def demo5():
    print("== 05. Связь многие-ко-многим: Article <-> Tag ==\n")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # --- Создаём статьи, теги и связи -----------------------------------------
    async with async_session() as session:
        python = Tag(name="python")
        async_t = Tag(name="async")
        db_t = Tag(name="db")
        a1 = Article(title="Введение в asyncio")
        a2 = Article(title="ORM за 10 минут")
        a3 = Article(title="Postgres для начинающих")
        session.add_all([python, async_t, db_t, a1, a2, a3])
        await session.flush()      # получаем id у всех объектов

        # Связь — это просто строки-пары в ассоциативной таблице. Пишем их явно.
        await session.execute(
            article_tags.insert().values([
                {"article_id": a1.id, "tag_id": python.id},
                {"article_id": a1.id, "tag_id": async_t.id},
                {"article_id": a2.id, "tag_id": python.id},
                {"article_id": a2.id, "tag_id": db_t.id},
                {"article_id": a3.id, "tag_id": db_t.id},
            ])
        )
        await session.commit()
        print("Создали 3 статьи, 3 тега и 5 пар-связей.\n")

    # --- Читаем статьи с тегами: JOIN по трём таблицам ------------------------
    async with async_session() as session:
        # articles -> article_tags -> tags. К столбцам ассоциативной таблицы
        # обращаемся через .c (article_tags.c.article_id).
        result = await session.execute(
            select(Article.title, Tag.name)
            .join(article_tags, article_tags.c.article_id == Article.id)
            .join(Tag, Tag.id == article_tags.c.tag_id)
            .order_by(Article.title, Tag.name)
        )
        print("Статья -> тег (через JOIN по трём таблицам):")
        for title, tag in result.all():
            print(f"  {title} -> {tag}")

    # --- Обратная сторона: какие статьи под тегом 'python' -------------------
    async with async_session() as session:
        result = await session.execute(
            select(Article.title)
            .join(article_tags, article_tags.c.article_id == Article.id)
            .join(Tag, Tag.id == article_tags.c.tag_id)
            .where(Tag.name == "python")
        )
        print("\nПод тегом 'python':", [row[0] for row in result.all()])

    # --- ORM-объекты + Pydantic ----------------------------------------------
    async with async_session() as session:
        articles = (await session.scalars(select(Article).order_by(Article.id))).all()
        print("\nСтатьи как объекты -> Pydantic:")
        for a in articles:
            print("  ", ArticleOut.model_validate(a).model_dump())

    await engine.dispose()
    print("\nИтог: многие-ко-многим = ассоциативная таблица из пар (article_id, tag_id);")
    print("чтобы собрать статьи с тегами, джойним три таблицы по ключам.")


if __name__ == "__main__":
    asyncio.run(demo5())
