"""Блок 1 (продолжение). Сырой SQL в PostgreSQL через asyncpg.

Здесь появляются две вещи, которых не было у SQLite:

1. ТАЙМАУТ НА ПОДКЛЮЧЕНИЕ. Postgres — это отдельный сервер, к которому мы идём
   ПО СЕТИ (сокет). Сервер может быть выключен, перегружен или недоступен —
   и тогда попытка подключиться будет висеть. Чтобы не зависнуть навсегда,
   подключение делают с таймаутом: "ждём коннект не дольше N секунд, иначе ошибка".

2. ПУЛ СОЕДИНЕНИЙ (connection pool). Открыть соединение с Postgres — дорого
   (TCP + аутентификация). Держать по соединению на каждый запрос расточительно.
   Пул открывает несколько соединений заранее и выдаёт их по требованию.

Запускать этот файл имеет смысл, когда рядом поднят Postgres. Проще всего — Docker:

    docker run --rm -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine

Если сервера нет — код не упадёт с трейсбеком, а поймает таймаут и объяснит, что
произошло (это и есть демонстрация таймаута в действии).

Обрати внимание на плейсхолдеры: у asyncpg это $1, $2, $3 (нумерованные), а НЕ "?"
как в SQLite. Синтаксис плейсхолдеров зависит от драйвера — это классическая
причина ошибок при переезде с одной БД на другую. ORM (файлы 03+) прячет эту
разницу: пишешь один код — он генерирует правильный SQL под нужную БД.
"""

import asyncio

import asyncpg

# Строка подключения (DSN). Формат: postgresql://user:password@host:port/dbname
DSN = "postgresql://postgres:postgres@localhost:5432/postgres"

# Сколько секунд ждём установки соединения, прежде чем сдаться.
CONNECT_TIMEOUT = 3.0


async def demo2():
    print("== 02. Сырой SQL в PostgreSQL (asyncpg) ==\n")

    # --- 1. Одиночное соединение с таймаутом -----------------------------------
    # timeout=... — максимум секунд на УСТАНОВКУ соединения. Не дождались —
    # asyncpg бросит исключение, а не зависнет.
    try:
        conn = await asyncpg.connect(DSN, timeout=CONNECT_TIMEOUT)
    except (OSError, asyncpg.PostgresError, asyncio.TimeoutError) as exc:
        # Сюда попадаем, если сервера нет / неверный пароль / не успели за таймаут.
        print(f"Не удалось подключиться к Postgres за {CONNECT_TIMEOUT} c: {exc!r}")
        print("Подними Postgres (см. docstring файла) и запусти снова.")
        return

    try:
        # Соединение открыто — работаем.
        await conn.execute("DROP TABLE IF EXISTS users")
        await conn.execute(
            """
            CREATE TABLE users (
                id    SERIAL PRIMARY KEY,
                name  TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )

        # Вставка с нумерованными плейсхолдерами $1, $2. Значения — позиционными
        # аргументами, НЕ склеиваем в строку (защита от SQL-инъекций).
        await conn.execute(
            "INSERT INTO users (name, email) VALUES ($1, $2)",
            "Иван", "ivan@example.com",
        )

        # executemany для пачки.
        await conn.executemany(
            "INSERT INTO users (name, email) VALUES ($1, $2)",
            [("Мария", "maria@example.com"), ("Олег", "oleg@example.com")],
        )
        print("Вставили 3 строки.\n")

        # fetch -> список Record; к полям можно обращаться по имени: row["name"].
        rows = await conn.fetch("SELECT id, name, email FROM users ORDER BY id")
        print("Все пользователи:")
        for row in rows:
            print(f"  id={row['id']} name={row['name']} email={row['email']}")

        # fetchrow -> одна строка (или None); fetchval -> одно значение.
        one = await conn.fetchrow("SELECT * FROM users WHERE email = $1", "maria@example.com")
        count = await conn.fetchval("SELECT count(*) FROM users")
        print("\nfetchrow:", dict(one))
        print("fetchval (count):", count)
    finally:
        # Соединение надо обязательно закрыть — иначе оно повиснет на сервере.
        await conn.close()

    # --- 2. Пул соединений + таймаут -------------------------------------------
    # create_pool заранее открывает от min_size до max_size соединений.
    # timeout здесь — таймаут на установку соединений пула.
    print("\n-- Пул соединений --")
    try:
        pool = await asyncpg.create_pool(
            DSN, min_size=1, max_size=5, timeout=CONNECT_TIMEOUT,
        )
    except (OSError, asyncpg.PostgresError, asyncio.TimeoutError) as exc:
        print(f"Пул не поднялся: {exc!r}")
        return

    try:
        # acquire() выдаёт свободное соединение из пула и возвращает его обратно
        # на выходе из блока. Это и есть "сессия" на время одной задачи:
        # взял соединение -> поработал -> вернул в пул для повторного использования.
        async with pool.acquire() as conn:
            total = await conn.fetchval("SELECT count(*) FROM users")
            print("В таблице сейчас строк:", total)
    finally:
        await pool.close()

    print("\nИтог: к серверной БД идём с таймаутом на коннект и через пул соединений.")
    print("Дальше пул и таймаут возьмёт на себя движок SQLAlchemy (файл 03).")


if __name__ == "__main__":
    asyncio.run(demo2())
