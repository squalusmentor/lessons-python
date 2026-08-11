"""Создание встречи через машину состояний и просмотр списка встреч.

Диалог создания: дата -> время -> описание. Каждый шаг — отдельное состояние;
дату и время до конца диалога держим в хранилище FSM и записываем в базу
одной строкой только на последнем шаге.
"""

from datetime import date, datetime, time
from html import escape

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import config, texts
from services.decorators import handle_resolver_errors
from services.repository import create_meeting, get_upcoming_meetings
from services.resolvers.keyboards import get_creation_keyboard, get_main_keyboard
from services.states import StateMachine
from services.utils import format_left, parse_date, parse_time


@handle_resolver_errors
async def resolve_create_request(message: Message, state: FSMContext):
    """Кнопка «Создать встречу» — входим в диалог и просим дату."""
    await state.set_state(StateMachine.meeting_waiting_date)
    example = datetime.now().strftime(config.DATE_FORMAT)
    await message.answer(
        texts.ASK_DATE.format(example=example), reply_markup=get_creation_keyboard()
    )


@handle_resolver_errors
async def resolve_date_entered(message: Message, state: FSMContext):
    """Шаг 1: разбираем дату и переходим к времени."""
    meeting_date = parse_date(message.text or "")
    example = datetime.now().strftime(config.DATE_FORMAT)

    if meeting_date is None:
        await message.answer(
            texts.ERROR_DATE_FORMAT.format(example=example),
            reply_markup=get_creation_keyboard(),
        )
        return

    if meeting_date < date.today():
        await message.answer(
            texts.ERROR_DATE_PAST, reply_markup=get_creation_keyboard()
        )
        return

    # В хранилище FSM кладём строку (оно сериализуемое), а не объект date
    await state.update_data(meeting_date=meeting_date.isoformat())
    await state.set_state(StateMachine.meeting_waiting_time)
    await message.answer(
        texts.ASK_TIME.format(date=meeting_date.strftime(config.DATE_FORMAT)),
        reply_markup=get_creation_keyboard(),
    )


@handle_resolver_errors
async def resolve_time_entered(message: Message, state: FSMContext):
    """Шаг 2: разбираем время, склеиваем с датой и просим описание."""
    meeting_time = parse_time(message.text or "")

    if meeting_time is None:
        await message.answer(
            texts.ERROR_TIME_FORMAT, reply_markup=get_creation_keyboard()
        )
        return

    data = await state.get_data()
    meeting_date = date.fromisoformat(data["meeting_date"])
    starts_at = datetime.combine(meeting_date, meeting_time)

    # Дату проверили на шаге 1, но «сегодня в 9 утра» в 18:00 — всё ещё прошлое
    if starts_at <= datetime.now():
        await message.answer(
            texts.ERROR_TIME_PAST, reply_markup=get_creation_keyboard()
        )
        return

    await state.update_data(meeting_time=meeting_time.isoformat(timespec="minutes"))
    await state.set_state(StateMachine.meeting_waiting_text)
    await message.answer(
        texts.ASK_TEXT.format(
            date=meeting_date.strftime(config.DATE_FORMAT),
            time=meeting_time.strftime(config.TIME_FORMAT),
        ),
        reply_markup=get_creation_keyboard(),
    )


@handle_resolver_errors
async def resolve_text_entered(message: Message, state: FSMContext):
    """Шаг 3: сохраняем встречу в базу и выходим из диалога."""
    text = (message.text or "").strip()

    if not text:
        await message.answer(
            texts.ERROR_TEXT_EMPTY, reply_markup=get_creation_keyboard()
        )
        return

    if len(text) > config.MAX_TEXT_LENGTH:
        await message.answer(
            texts.ERROR_TEXT_LONG.format(limit=config.MAX_TEXT_LENGTH),
            reply_markup=get_creation_keyboard(),
        )
        return

    data = await state.get_data()
    starts_at = datetime.combine(
        date.fromisoformat(data["meeting_date"]),
        time.fromisoformat(data["meeting_time"]),
    )

    await create_meeting(
        user_id=message.from_user.id,
        username=message.from_user.username,
        starts_at=starts_at,
        text=text,
    )

    await state.clear()
    await message.answer(
        texts.MEETING_CREATED.format(
            date=starts_at.strftime(config.DATE_FORMAT),
            time=starts_at.strftime(config.TIME_FORMAT),
            text=escape(text),
        ),
        reply_markup=get_main_keyboard(),
    )


@handle_resolver_errors
async def resolve_cancel(message: Message, state: FSMContext):
    """Кнопка «Отмена» — выходим из диалога, ничего не сохраняя."""
    if await state.get_state() is None:
        await message.answer(texts.NOTHING_TO_CANCEL, reply_markup=get_main_keyboard())
        return

    await state.clear()
    await message.answer(texts.CANCELLED, reply_markup=get_main_keyboard())


@handle_resolver_errors
async def resolve_list(message: Message, state: FSMContext):
    """Кнопка «Все встречи» — показывает будущие встречи пользователя.

    Нажатие в середине диалога создания прерывает его: иначе пользователь
    увидел бы список и остался в состоянии «жду время», не понимая этого.
    """
    await state.clear()

    meetings = await get_upcoming_meetings(message.from_user.id)
    if not meetings:
        await message.answer(texts.MEETINGS_EMPTY, reply_markup=get_main_keyboard())
        return

    now = datetime.now()
    lines = [texts.MEETINGS_HEADER]
    for index, meeting in enumerate(meetings, start=1):
        lines.append(
            texts.MEETINGS_ITEM.format(
                index=index,
                date=meeting.starts_at.strftime(config.DATE_FORMAT),
                time=meeting.starts_at.strftime(config.TIME_FORMAT),
                left=format_left(meeting.starts_at - now),
                text=escape(meeting.text),
            )
        )

    await message.answer("".join(lines), reply_markup=get_main_keyboard())
