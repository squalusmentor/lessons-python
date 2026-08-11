from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from services.db import Base


class Meeting(Base):
    """Встреча, созданная пользователем.

    Время храним наивным (без таймзоны) в локальном времени сервера — с ним же
    сравниваем datetime.now() в планировщике. Для урока этого достаточно;
    в боевом боте у каждого пользователя была бы своя таймзона, а в базе — UTC.
    """

    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Telegram id пользователя. В личном чате он же является chat_id —
    # именно по нему планировщик отправляет напоминание.
    user_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Дата и время начала встречи
    starts_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    # Флаг «напоминание уже отправлено». Без него встреча, попавшая в окно
    # «меньше двух часов», ловилась бы двумя соседними часовыми проверками
    # и пользователь получил бы два одинаковых сообщения.
    reminded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    def __repr__(self) -> str:
        return f"Meeting(id={self.id}, user_id={self.user_id}, starts_at={self.starts_at})"
