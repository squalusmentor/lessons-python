"""Фоновый планировщик напоминаний.

Идея: обычный поток раз в час просит event loop бота выполнить корутину,
которая заглядывает в базу и рассылает напоминания.

Почему поток, а не asyncio.create_task с asyncio.sleep? Технически задачу можно
решить и так. Здесь поток взят намеренно — чтобы показать мост между обычным
кодом и циклом событий:

- поток спит на threading.Event.wait() — это блокирующее ожидание, в корутине
  такое замораживало бы весь бот;
- саму работу (запросы к базе, отправка сообщений) поток НЕ делает: он отдаёт
  корутину в чужой event loop через asyncio.run_coroutine_threadsafe.

Это единственный безопасный способ дотянуться до event loop из другого потока:
почти все объекты asyncio не потокобезопасны, и вызывать их методы напрямую
из стороннего потока нельзя. run_coroutine_threadsafe ставит корутину в
очередь loop'а и возвращает concurrent.futures.Future — обычный, «потоковый»,
у которого result() блокирует вызывающий поток, а не цикл событий.

Так и появляется формулировка «отдельный поток отправляет таску в тот же event
loop, где крутится бот»: бот и напоминания живут в одном цикле и делят одно
подключение к базе, а расписанием заведует поток снаружи.
"""

import asyncio
import threading
from datetime import datetime, timedelta
from html import escape

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from loguru import logger

from config import config, texts
from services.repository import get_meetings_to_remind, mark_reminded
from services.resolvers.keyboards import get_main_keyboard
from services.utils import format_left


async def send_reminders(bot: Bot):
    """Одна проверка: кому пора напомнить о встрече.

    Выполняется в event loop бота, поэтому спокойно ходит в базу через await
    и пользуется тем же объектом Bot, что и обработчики сообщений.
    """
    window = timedelta(hours=config.REMINDER_WINDOW_HOURS)
    meetings = await get_meetings_to_remind(window)

    if not meetings:
        logger.info("Проверка напоминаний: подходящих встреч нет")
        return

    logger.info(f"Проверка напоминаний: найдено {len(meetings)} встреч(и)")
    delivered = []

    for meeting in meetings:
        try:
            # В личном чате chat_id совпадает с telegram id пользователя
            await bot.send_message(
                chat_id=meeting.user_id,
                text=texts.REMINDER.format(
                    date=meeting.starts_at.strftime(config.DATE_FORMAT),
                    time=meeting.starts_at.strftime(config.TIME_FORMAT),
                    text=escape(meeting.text),
                    left=format_left(meeting.starts_at - datetime.now()),
                ),
                reply_markup=get_main_keyboard(),
            )
            delivered.append(meeting.id)
        except TelegramAPIError as e:
            # Пользователь мог заблокировать бота — не роняем из-за этого рассылку
            logger.warning(f"Не смогли напомнить пользователю {meeting.user_id}: {e}")

    # Помечаем только доставленные: недоставленные попробуем через час снова
    await mark_reminded(delivered)
    logger.info(f"Напоминаний отправлено: {len(delivered)}")


class ReminderScheduler:
    """Поток-расписание: раз в интервал кидает send_reminders в event loop бота."""

    def __init__(self, bot: Bot, loop: asyncio.AbstractEventLoop):
        self._bot = bot
        # Тот самый loop, в котором работает поллинг бота
        self._loop = loop
        # Event вместо time.sleep: даёт прервать ожидание при остановке бота
        self._stop_event = threading.Event()
        # daemon=True — поток не помешает процессу завершиться
        self._thread = threading.Thread(
            target=self._worker, name="reminder-scheduler", daemon=True
        )

    def start(self):
        self._thread.start()
        logger.info(
            f"Планировщик напоминаний запущен: проверка раз в "
            f"{config.REMINDER_INTERVAL_SEC} c, окно {config.REMINDER_WINDOW_HOURS} ч"
        )

    def stop(self):
        self._stop_event.set()
        self._thread.join(timeout=5)
        logger.info("Планировщик напоминаний остановлен")

    def _worker(self):
        """Тело потока: проверяем сразу на старте, дальше — раз в интервал."""
        while True:
            self._submit_check()
            # wait вернёт True, если за время ожидания позвали stop()
            if self._stop_event.wait(timeout=config.REMINDER_INTERVAL_SEC):
                return

    def _submit_check(self):
        """Отдаёт корутину в event loop бота и дожидается результата."""
        future = asyncio.run_coroutine_threadsafe(send_reminders(self._bot), self._loop)
        try:
            # Ждём здесь, в своём потоке: во-первых, чтобы увидеть исключение
            # из корутины, во-вторых, чтобы проверки не наезжали друг на друга.
            future.result(timeout=config.REMINDER_TASK_TIMEOUT_SEC)
        except Exception as e:
            logger.exception(f"Ошибка при рассылке напоминаний: {e}")
