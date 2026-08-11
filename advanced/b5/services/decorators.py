"""Декораторы для обработчиков."""

from functools import wraps

from aiogram.types import CallbackQuery, Message
from loguru import logger

from config import texts


def handle_resolver_errors(func):
    """Ловит любое исключение внутри резолвера.

    Без него необработанная ошибка просто уедет в лог aiogram, а пользователь
    останется молча смотреть в экран. С ним — в логе трейсбек, в чате понятное
    сообщение.
    """

    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        try:
            return await func(event, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Ошибка в {func.__name__}: {e}")
            if isinstance(event, Message):
                await event.answer(texts.ERROR)
            elif isinstance(event, CallbackQuery):
                await event.message.answer(texts.ERROR)

    return wrapper
