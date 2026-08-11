import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from config import config
from services.db_connect import dispose_db, init_db
from services.handlers import setup_router
from services.scheduler import ReminderScheduler


async def main():
    """Запуск"""
    logger.info("Запуск бота...")
    if not config.token:
        logger.error("BOT_TOKEN не задан — положи токен в .env рядом с main.py")
        return

    await init_db()

    # parse_mode=HTML включает разметку для всех сообщений сразу,
    # чтобы не передавать его в каждый answer()
    bot = Bot(
        token=config.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(setup_router())

    # Отдаём планировщику текущий event loop — тот самый, в котором дальше
    # будет крутиться поллинг. Его поток будет класть в этот loop задачи.
    scheduler = ReminderScheduler(bot=bot, loop=asyncio.get_running_loop())
    scheduler.start()

    try:
        logger.info("Бот запущен!")
        await dp.start_polling(bot)
    finally:
        scheduler.stop()
        await dispose_db()
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.exception(f"Критическая ошибка: {e}")
