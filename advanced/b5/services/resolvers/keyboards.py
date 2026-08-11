"""Клавиатуры бота.

Здесь только ReplyKeyboardMarkup — «нижняя панель» под полем ввода. В отличие
от инлайн-кнопок она не привязана к конкретному сообщению и остаётся на экране
постоянно, поэтому её и прикладываем к каждому ответу бота.
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config.config import BTN_CANCEL, BTN_CREATE, BTN_LIST


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Основная панель: доступна на любом шаге диалога."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CREATE), KeyboardButton(text=BTN_LIST)]],
        # resize_keyboard подгоняет высоту под содержимое,
        # is_persistent не даёт панели прятаться за обычной клавиатурой
        resize_keyboard=True,
        is_persistent=True,
    )


def get_creation_keyboard() -> ReplyKeyboardMarkup:
    """Та же панель плюс «Отмена» — показывается на шагах создания встречи."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_CREATE), KeyboardButton(text=BTN_LIST)],
            [KeyboardButton(text=BTN_CANCEL)],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )
