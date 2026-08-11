"""Единственное место, где проект ходит в базу.

Резолверы и планировщик вызывают функции отсюда и получают готовые объекты —
им не нужно знать ни про сессии, ни про select(). Ровно та же идея, что в
референс-проекте с его api_requests.py, только за слоем не HTTP, а SQLite.
"""

from datetime import datetime, timedelta

from sqlalchemy import select, update

from services.db_connect import async_session
from services.models.meeting import Meeting


async def create_meeting(
    user_id: int, username: str | None, starts_at: datetime, text: str
) -> Meeting:
    """Сохраняет новую встречу и возвращает её уже с присвоенным id."""
    async with async_session() as session:
        meeting = Meeting(
            user_id=user_id, username=username, starts_at=starts_at, text=text
        )
        session.add(meeting)
        await session.commit()
        return meeting


async def get_upcoming_meetings(user_id: int) -> list[Meeting]:
    """Будущие встречи одного пользователя, от ближайшей к дальней."""
    async with async_session() as session:
        result = await session.execute(
            select(Meeting)
            .where(Meeting.user_id == user_id, Meeting.starts_at >= datetime.now())
            .order_by(Meeting.starts_at)
        )
        return list(result.scalars().all())


async def get_meetings_to_remind(window: timedelta) -> list[Meeting]:
    """Встречи всех пользователей, которые начнутся в ближайшее окно.

    Берём только те, о которых ещё не напоминали (reminded == False), чтобы
    следующая часовая проверка не прислала второе такое же сообщение.
    """
    now = datetime.now()
    async with async_session() as session:
        result = await session.execute(
            select(Meeting)
            .where(
                Meeting.reminded.is_(False),
                Meeting.starts_at > now,
                Meeting.starts_at <= now + window,
            )
            .order_by(Meeting.starts_at)
        )
        return list(result.scalars().all())


async def mark_reminded(meeting_ids: list[int]) -> None:
    """Помечает встречи как «напоминание доставлено» одним UPDATE."""
    if not meeting_ids:
        return

    async with async_session() as session:
        await session.execute(
            update(Meeting).where(Meeting.id.in_(meeting_ids)).values(reminded=True)
        )
        await session.commit()
