"""Мелкие помощники: разбор ввода пользователя и форматирование сроков."""

from datetime import date, datetime, time, timedelta

from config import config


def parse_date(raw: str) -> date | None:
    """Строка «ДД.ММ.ГГГГ» -> date. None, если формат не подошёл."""
    try:
        return datetime.strptime(raw.strip(), config.DATE_FORMAT).date()
    except ValueError:
        return None


def parse_time(raw: str) -> time | None:
    """Строка «ЧЧ:ММ» -> time. None, если формат не подошёл."""
    try:
        return datetime.strptime(raw.strip(), config.TIME_FORMAT).time()
    except ValueError:
        return None


def format_left(delta: timedelta) -> str:
    """Сколько осталось до встречи, человеческим текстом: «1 ч 45 мин»."""
    minutes = int(delta.total_seconds() // 60)
    if minutes <= 0:
        return "меньше минуты"

    days, rest = divmod(minutes, 24 * 60)
    hours, mins = divmod(rest, 60)

    parts = []
    if days:
        parts.append(f"{days} д")
    if hours:
        parts.append(f"{hours} ч")
    # Минуты показываем, если они есть или если больше показать нечего
    if mins or not parts:
        parts.append(f"{mins} мин")
    return " ".join(parts)
