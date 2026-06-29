from asyncio import sleep

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from loguru import logger
import asyncpg

from source.config import settings
from source.db import Base
from source.models.user import User
from source.models.article import Article
from source.services.seed import seed_database


engine = create_async_engine(settings.databese_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def _create_database_if_not_exists():
    # подключаемся к системной postgres, создаём нашу БД если нет
    try:
        conn = await asyncpg.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database="postgres",
        )
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", settings.DB_NAME
        )
        if not exists:
            await conn.execute(f'CREATE DATABASE "{settings.DB_NAME}"')
            logger.info(f"Database '{settings.DB_NAME}' created")
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise
    finally:
        await conn.close()


async def connect_with_retry():
    while True:
        try:
            await _create_database_if_not_exists()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database connected, tables ready")

            if settings.SEED_DB:
                await seed_database(async_session)

            break
        except Exception as e:
            logger.warning(f"Cannot connect to database: {e}. Retrying in 5s...")
            await sleep(5)


async def disconnect():
    await engine.dispose()
    logger.info("Database disconnected")
