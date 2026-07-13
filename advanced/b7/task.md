# Практическое задание B7 — мини-библиотека на async ORM

Собери маленькое консольное приложение «библиотека» на **SQLAlchemy 2.0 (async)**.
Базой возьми **SQLite** (`sqlite+aiosqlite:///library.db`) — ничего поднимать не
надо. Весь код — асинхронный (`async def`, `await`, `asyncio.run(...)`).

Цель — своими руками пройти всё из урока: движок и сессия, CRUD, обе связи
(один-ко-многим и многие-ко-многим), мост ORM -> Pydantic.

## Схема данных

Три сущности и связи между ними:

- **Author** (автор): `id`, `name`.
- **Book** (книга): `id`, `title`, `year`, `author_id` -> `authors.id`.
  Связь **один-ко-многим**: у автора много книг, книга принадлежит одному автору.
- **Genre** (жанр): `id`, `name` (уникальное).
  Связь **многие-ко-многим** с книгами через ассоциативную таблицу `book_genres`:
  у книги несколько жанров, у жанра несколько книг.

## Что должно уметь приложение

Оформи как набор `async`-функций, вызови их по очереди из одной точки входа:

1. **Создать таблицы** заново при старте (`drop_all` + `create_all`).
2. **Заполнить данными**: минимум 2 автора, 4 книги, 3 жанра; проставить связи
   (книгам — `author_id`, а в ассоциативную таблицу `book_genres` — пары
   книга-жанр). `id` до `commit` бери через `flush`.
3. **Вывести всех авторов с их книгами** — обычным `JOIN` (`authors` + `books`).
4. **Найти книгу по названию** и вывести её автора и список жанров (тоже JOIN'ами).
5. **Вывести все книги одного жанра** (JOIN по трём таблицам с `WHERE genre.name = ...`).
6. **Обновить** год у одной книги и **удалить** одну книгу; показать, что
   изменения применились.
7. **Отдать наружу через Pydantic**: собери плоскую схему `BookOut`
   (`id`, `title`, `year`, `author_id`), достань книги как объекты
   (`select(Book)`), провалидируй и напечатай `model_dump()`.

## Требования

- Модели — в стиле урока: `DeclarativeBase`, `Mapped`, `mapped_column`,
  `ForeignKey(...)`, `Table` для связи многие-ко-многим.
- Работа с БД — только через сессию (`async_sessionmaker`, `async with ... as session`).
- Связанные данные читаем **обычным JOIN** (`select(...).join(...)`), как в
  `04`/`05` — без `relationship()` и `selectinload`.
- Pydantic-схемы с `model_config = ConfigDict(from_attributes=True)`.
- `requirements.txt` — как минимум `sqlalchemy[asyncio]`, `aiosqlite`, `pydantic`.
- Осмысленные коммиты (`init`, `add models`, `add joins`, `add pydantic schemas`).

## Подсказки

- Сначала автор, потом книги с его `id`:

  ```python
  author = Author(name="Стругацкие")
  session.add(author)
  await session.flush()                          # author.id теперь известен
  session.add(Book(title="Пикник", year=1972, author_id=author.id))
  await session.commit()
  ```

- Авторы вместе с книгами — JOIN:

  ```python
  result = await session.execute(
      select(Author.name, Book.title).join(Book, Book.author_id == Author.id)
  )
  for name, title in result.all():
      print(name, "->", title)
  ```

- Связь многие-ко-многим — пары в ассоциативной таблице (см. `05_orm_many_to_many.py`):

  ```python
  await session.execute(book_genres.insert().values(book_id=b.id, genre_id=g.id))
  ```

## Со звёздочкой (по желанию)

- Переключи проект на **Postgres**, поменяв ТОЛЬКО URL движка на
  `postgresql+asyncpg://...` (подними Postgres в Docker, как в `02_raw_postgres.py`).
  Убедись, что весь остальной код остался нетронутым — в этом сила ORM.
- **Продвинутый уровень связей**: замени ручные JOIN'ы на `relationship()` и
  жадную загрузку `selectinload`, чтобы ходить по связи как по списку
  (`author.books`), и собери **вложенную** схему `AuthorWithBooks`.
- Заведи `config.py` c `pydantic-settings` (как в референс-проекте): читай
  параметры БД из переменных окружения и собирай URL свойством.
- Добавь функцию `connect_with_retry()` — подключение к БД с несколькими попытками
  и паузой между ними (на случай, когда Postgres ещё поднимается).
