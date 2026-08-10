import os
from pathlib import Path

from dotenv import load_dotenv

# Корень проекта — папка b9 (на уровень выше этого файла)
BASE_DIR = Path(__file__).parent.parent

# Загружаем переменные из .env. Путь указываем явно, чтобы бот запускался
# из любой рабочей директории, а не только из папки проекта.
load_dotenv(BASE_DIR / ".env")

token = os.getenv("BOT_TOKEN", "")

# База — обычный файл рядом с main.py. sqlite+aiosqlite — async-драйвер из B7:
# он не блокирует event loop, в котором крутится поллинг бота.
DB_PATH = BASE_DIR / "meetings.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# === Напоминания === #
# Как часто фоновый поток просит бота заглянуть в базу
REMINDER_INTERVAL_SEC = 60 * 60
# Напоминаем о встречах, до которых осталось меньше стольких часов.
# Окно (2 ч) больше интервала опроса (1 ч) — поэтому ни одна встреча не
# проскочит между проверками, и напоминание приходит за 1-2 часа до начала.
REMINDER_WINDOW_HOURS = 2
# Сколько фоновый поток ждёт результат задачи, отданной в event loop
REMINDER_TASK_TIMEOUT_SEC = 60

# === Формат ввода === #
DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"
MAX_TEXT_LENGTH = 500

# === Кнопки нижней панели === #
# Единый источник меток: и клавиатуры, и фильтры обработчиков смотрят сюда.
BTN_CREATE = "📅 Создать встречу"
BTN_LIST = "📋 Все встречи"
BTN_CANCEL = "❌ Отмена"
