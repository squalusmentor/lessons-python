"""Точка входа урока B3.

Файлы начинаются с цифры — обычным import их не подключить, поэтому грузим модуль
напрямую по пути через importlib (как в уроке L6). Раскомментируй нужную строку и
запусти: python main.py

Каждый файл запускается и напрямую, например: python 03_orm_intro.py
"""

import asyncio
import importlib.util
from pathlib import Path


def _load(filename: str):
    path = Path(__file__).parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Демо-функции асинхронные — оборачиваем в asyncio.run(...).

# --- Блок 1. Сырой SQL и асинхронные коннекторы ---
asyncio.run(_load("01_raw_sqlite.py").demo1())        # aiosqlite: SQLite-файл
# asyncio.run(_load("02_raw_postgres.py").demo2())    # asyncpg: Postgres, таймаут, пул

# --- Блок 2. ORM (SQLAlchemy 2.0 async) + Pydantic ---
# asyncio.run(_load("03_orm_intro.py").demo3())        # движок, сессия, CRUD, схемы
# asyncio.run(_load("04_orm_relationships.py").demo4()) # связь один-ко-многим
# asyncio.run(_load("05_orm_many_to_many.py").demo5())  # связь многие-ко-многим
