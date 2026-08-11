"""Приветствие, справка и всё, что не попало в остальные обработчики."""

from html import escape

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import texts
from services.decorators import handle_resolver_errors
from services.resolvers.keyboards import get_main_keyboard


@handle_resolver_errors
async def resolve_start(message: Message, state: FSMContext):
    """Команда /start — сбрасывает диалог и показывает нижнюю панель."""
    await state.clear()
    # Имя приходит от пользователя, поэтому экранируем: иначе «<Вася>»
    # в имени сломает HTML-разметку сообщения.
    name = escape(message.from_user.first_name or "гость")
    await message.answer(texts.START.format(name=name), reply_markup=get_main_keyboard())


@handle_resolver_errors
async def resolve_help(message: Message):
    """Команда /help — та же справка, но без сброса состояния."""
    await message.answer(texts.HELP, reply_markup=get_main_keyboard())


@handle_resolver_errors
async def resolve_unknown(message: Message):
    """Последний обработчик: сюда попадает всё, что не разобрали выше."""
    await message.answer(texts.UNKNOWN, reply_markup=get_main_keyboard())
