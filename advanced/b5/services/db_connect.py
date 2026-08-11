from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config
from services.db import Base
# Импорт модели обязателен: пока модуль не выполнен, таблицы нет в
# Base.metadata и create_all её не создаст.
from services.models.meeting import Meeting  # noqa: F401


# Движок держит пул соединений к файлу базы. Создаётся один раз на приложение.
engine = create_async_engine(config.DATABASE_URL, echo=False)

# expire_on_commit=False — после commit объекты остаются пригодными к чтению
# и не лезут в базу за свежими значениями (в async это стоило бы отдельного await).
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    """Создаёт таблицы, если их ещё нет.

    create_all — синхронная операция, поэтому исполняем её через run_sync
    на асинхронном соединении. В боевом проекте вместо этого были бы миграции
    (Alembic), но для урока достаточно.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info(f"База готова: {config.DB_PATH}")


async def dispose_db():
    """Закрывает пул соединений при остановке бота."""
    await engine.dispose()
    logger.info("Соединение с базой закрыто")
