from loguru import logger
from sqlalchemy import select

from sqlalchemy.ext.asyncio import async_sessionmaker
from source.models.user import User
from source.models.article import Article
from source.services.scripts import hash_password


async def seed_database(async_session: async_sessionmaker):
    async with async_session() as session:

        # проверяем — если данные уже есть, не заполняем повторно
        existing = await session.scalar(select(User))
        if existing:
            logger.info("Database already seeded, skipping")
            return

        # --- пользователи ---
        admin = User(
            first_name="User1",
            last_name="Admin",
            middle_name="Administrator",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            is_active=True,
            is_admin=True,
        )
        user1 = User(
            first_name="User2",
            last_name="User",
            middle_name="User",
            email="user2@example.com",
            password_hash=hash_password("user123"),
            is_active=True,
            is_admin=False,
        )
        user2 = User(
            first_name="User3",
            last_name="User",
            middle_name=None,
            email="user3@example.com",
            password_hash=hash_password("user123"),
            is_active=True,
            is_admin=False,
        )

        session.add_all([admin, user1, user2])
        await session.flush()

        # --- статьи ---
        articles = [
            Article(
                title="Статья 1",
                content="Текст статьи 1. Это пример статьи, написанной администратором",
                owner_id=admin.id,
            ),
            Article(
                title="Статья 2",
                content="Текст статьи 2. Это пример статьи, написанной администратором",
                owner_id=admin.id,
            ),
            Article(
                title="Статья 3",
                content="Текст статьи 3. Это пример статьи, написанной обычным пользователем",
                owner_id=user1.id,
            ),
            Article(
                title="Статья 4",
                content="Текст статьи 4. Это пример статьи, написанной обычным пользователем",
                owner_id=user1.id,
            ),
            Article(
                title="Статья 5",
                content="Текст статьи 5. Это пример статьи, написанной обычным пользователем",
                owner_id=user2.id,
            ),
        ]

        session.add_all(articles)
        await session.commit()

    logger.info("Database seeded: 3 users, 5 articles")
