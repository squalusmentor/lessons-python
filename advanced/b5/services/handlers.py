"""Регистрация обработчиков.

Здесь только маршрутизация: какой апдейт какому резолверу отдать. Вся логика
живёт в services/resolvers/ — так обработчики остаются читаемым оглавлением
бота, а не свалкой кода.

ПОРЯДОК РЕГИСТРАЦИИ ВАЖЕН. aiogram проверяет обработчики сверху вниз и отдаёт
апдейт первому подошедшему. Поэтому кнопки нижней панели ловим ДО состояний:
иначе нажатие «Все встречи» на шаге ввода описания сохранилось бы как текст
встречи. По той же причине обработчик без фильтров стоит последним.
"""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.config import BTN_CANCEL, BTN_CREATE, BTN_LIST
from services.resolvers.common import resolve_help, resolve_start, resolve_unknown
from services.resolvers.meetings import (
    resolve_cancel,
    resolve_create_request,
    resolve_date_entered,
    resolve_list,
    resolve_text_entered,
    resolve_time_entered,
)
from services.states import StateMachine

router = Router()


def setup_router():
    """Настройка обработчиков сообщений"""

    # === КОМАНДЫ === #

    @router.message(CommandStart())
    async def cmd_start(message: Message, state: FSMContext):
        await resolve_start(message, state)

    @router.message(Command("help"))
    async def cmd_help(message: Message):
        await resolve_help(message)

    # === КНОПКИ НИЖНЕЙ ПАНЕЛИ === #
    # Зарегистрированы до состояний, чтобы работать на любом шаге диалога.

    @router.message(F.text == BTN_CREATE)
    async def btn_create(message: Message, state: FSMContext):
        await resolve_create_request(message, state)

    @router.message(F.text == BTN_LIST)
    async def btn_list(message: Message, state: FSMContext):
        await resolve_list(message, state)

    @router.message(F.text == BTN_CANCEL)
    async def btn_cancel(message: Message, state: FSMContext):
        await resolve_cancel(message, state)

    # === СОЗДАНИЕ ВСТРЕЧИ: дата -> время -> описание === #

    @router.message(StateMachine.meeting_waiting_date)
    async def meeting_date(message: Message, state: FSMContext):
        await resolve_date_entered(message, state)

    @router.message(StateMachine.meeting_waiting_time)
    async def meeting_time(message: Message, state: FSMContext):
        await resolve_time_entered(message, state)

    @router.message(StateMachine.meeting_waiting_text)
    async def meeting_text(message: Message, state: FSMContext):
        await resolve_text_entered(message, state)

    # === ВСЁ ОСТАЛЬНОЕ (последний обработчик!) === #

    @router.message()
    async def other_message(message: Message):
        await resolve_unknown(message)

    return router
