"""Блок 1. Сырой SQL в SQLite через асинхронный драйвер aiosqlite.

Начинаем с самого низкого уровня: пишем SQL руками и сами разбираем ответ.
ORM появится позже (файлы 03-05) — но чтобы понимать, что он делает за тебя,
сначала надо увидеть, как это выглядит без него.

SQLite — встроенная БД: это ОДИН ФАЙЛ на диске, отдельного сервера нет. Драйвер
просто открывает файл. Поэтому "таймаут на подключение" тут почти не при делах
(подключаться некуда по сети) — эта тема раскроется в 02 на Postgres.

Почему aiosqlite, а не стандартный sqlite3? Модуль sqlite3 из стандартной
библиотеки — СИНХРОННЫЙ: его вызовы блокируют event loop (см. теорию про event
loop в уроке B2). aiosqlite — тонкая асинхронная обёртка: те же курсоры и методы,
но каждый вызывается через await и не вешает loop.
"""

import asyncio
from pathlib import Path

import aiosqlite

# Кладём файл БД рядом со скриптом. Каждый запуск начинаем с чистого листа.
DB_PATH = Path(__file__).parent / "demo_sqlite.db"


async def demo1():
    print("== 01. Сырой SQL в SQLite (aiosqlite) ==\n")

    # aiosqlite.connect(...) — асинхронный контекстный менеджер. На входе открывает
    # файл-БД, на выходе гарантированно закрывает соединение.
    async with aiosqlite.connect(DB_PATH) as db:

        # --- 1. Создаём таблицу -------------------------------------------------
        # DROP ... IF EXISTS делает демо идемпотентным: можно запускать сколько угодно.
        await db.execute("DROP TABLE IF EXISTS users")
        await db.execute(
            """
            CREATE TABLE users (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                email TEXT    NOT NULL UNIQUE
            )
            """
        )

        # --- 2. Вставка. Параметры — ТОЛЬКО через плейсхолдеры ------------------
        # Плейсхолдер SQLite — знак "?". Значения передаём вторым аргументом кортежем.
        # НИКОГДА не склеивай значения в строку через f"...{name}..." — это дыра для
        # SQL-инъекции. Драйвер сам экранирует данные, если отдать их отдельно.
        await db.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            ("Иван", "ivan@example.com"),
        )

        # executemany — вставка пачки строк одним вызовом.
        await db.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            [
                ("Мария", "maria@example.com"),
                ("Олег", "oleg@example.com"),
            ],
        )

        # Важно: до commit() изменения живут только в нашей транзакции. commit()
        # фиксирует их в файле. Без него после закрытия соединения данных не будет.
        await db.commit()
        print("Вставили 3 строки, commit сделан.\n")

        # --- 3. Чтение. fetchall / fetchone ------------------------------------
        # execute на SELECT возвращает курсор — по нему забираем строки.
        async with db.execute("SELECT id, name, email FROM users") as cursor:
            rows = await cursor.fetchall()          # список кортежей
            print("Все пользователи (кортежи):")
            for row in rows:
                print("  ", row)                    # (1, 'Иван', 'ivan@example.com')

        # fetchone — одна строка (или None, если ничего не нашлось).
        async with db.execute(
            "SELECT id, name FROM users WHERE email = ?",
            ("maria@example.com",),                 # кортеж из одного элемента: (x,)
        ) as cursor:
            one = await cursor.fetchone()
            print("\nПоиск по email:", one)

        # --- 4. row_factory: строки по имени столбца, а не по индексу ----------
        # По умолчанию строка — кортеж, поля берём по номеру row[1]. Неудобно и
        # хрупко. row_factory = aiosqlite.Row даёт доступ по имени: row["name"].
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE name = ?", ("Олег",)) as cur:
            r = await cur.fetchone()
            print("\nЧерез Row по имени столбца:")
            print("  id =", r["id"], "| name =", r["name"], "| email =", r["email"])

        # --- 5. UPDATE и DELETE, rowcount --------------------------------------
        cur = await db.execute(
            "UPDATE users SET name = ? WHERE email = ?",
            ("Иван Петров", "ivan@example.com"),
        )
        await db.commit()
        print("\nUPDATE затронул строк:", cur.rowcount)

        cur = await db.execute("DELETE FROM users WHERE name = ?", ("Олег",))
        await db.commit()
        print("DELETE затронул строк:", cur.rowcount)

    print("\nИтог: сырой SQL = ты сам пишешь запросы и сам разбираешь кортежи.")
    print("Дальше (03) тем же займётся ORM, но вернёт готовые объекты, а не кортежи.")


if __name__ == "__main__":
    asyncio.run(demo1())
