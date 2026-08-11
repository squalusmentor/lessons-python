# Урок B3. Базы данных: сырой SQL, async-драйверы и ORM (SQLAlchemy + Pydantic)

В B2 мы подняли API на FastAPI, но данные брали из списка в памяти — «вместо базы».
Там же было обещано: *«сегодня сервис отдаёт статику, завтра ходит в PostgreSQL —
меняется только слой `services/`»*. Этот урок — про то самое «завтра». Учимся
хранить данные в настоящей БД и доставать их **не блокируя event loop**.

Идём снизу вверх, от «руками» к «за тебя»:

1. **Сырой SQL** через асинхронные драйверы — чтобы увидеть, что происходит на
   самом низком уровне (файлы `01`, `02`). Сразу две БД: **SQLite** и **PostgreSQL**.
2. **ORM SQLAlchemy 2.0 (async)** — тот же CRUD, но объектами вместо строк-кортежей,
   плюс мост в **Pydantic** (файл `03`).
3. **Связи между таблицами** — один-ко-многим и многие-ко-многим (файлы `04`, `05`).

Урок опирается на теорию **event loop и GIL** из B2 — если подзабыл, почему БД-вызовы
обязаны быть асинхронными, перечитай третью часть B2.

## Структура урока

```
b3/
├── readme.md                   — этот файл (теория)
├── to-do.md                    — практическое задание (мини-библиотека)
├── requirements.txt            — зависимости (aiosqlite, asyncpg, sqlalchemy, pydantic)
├── main.py                     — точка входа: раскомментируй нужное демо
│
│   --- Блок 1. Сырой SQL и async-драйверы ---
├── 01_raw_sqlite.py            — aiosqlite: SQLite-файл, курсоры, параметры   (demo1)
├── 02_raw_postgres.py          — asyncpg: Postgres, таймаут коннекта, пул     (demo2)
│
│   --- Блок 2. ORM (SQLAlchemy 2.0 async) + Pydantic ---
├── 03_orm_intro.py             — движок, сессия, CRUD, мост в Pydantic        (demo3)
├── 04_orm_relationships.py     — связь один-ко-многим (User -> Articles)      (demo4)
└── 05_orm_many_to_many.py      — связь многие-ко-многим (Article <-> Tag)     (demo5)
```

### Запуск

```bash
pip install -r requirements.txt
python main.py                 # раскомментируй нужную строку внутри
# или каждый файл напрямую:
python 03_orm_intro.py
```

Файлы `01`, `03`, `04`, `05` работают на **SQLite** — им ничего поднимать не надо,
БД это просто файл рядом со скриптом. Файл `02` идёт в **PostgreSQL**; чтобы его
попробовать, подними сервер (проще всего Docker):

```bash
docker run --rm -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:16-alpine
```

Если Postgres не поднят — `02` не упадёт с трейсбеком, а поймает таймаут и объяснит,
что произошло (это и есть демонстрация таймаута).

---

# Часть 1. БД, драйверы и сырой SQL

## Два вида баз: встроенная и серверная

| | **SQLite** | **PostgreSQL** |
|---|---|---|
| Что это | библиотека, БД = **один файл** | отдельный **сервер-процесс** |
| Куда подключаемся | открываем файл на диске | идём **по сети** (сокет, порт 5432) |
| Установка | не нужна, встроена в Python | нужен сервер (пакет/Docker) |
| Таймаут коннекта | почти не нужен (файл рядом) | **нужен** — сеть может не ответить |
| Для чего | тесты, прототипы, локалка, десктоп | боевые приложения, много клиентов |

Ключевая разница для нас: к SQLite мы просто **открываем файл**, а к Postgres —
**подключаемся по сети**, и это подключение может не состояться (сервер выключен,
перегружен, недоступен). Отсюда — тема таймаутов и пулов ниже.

## Почему драйверы асинхронные

Из B2: FastAPI крутится на **одном потоке** в event loop. Если внутри `async def`
позвать **синхронный** (блокирующий) драйвер БД, весь loop замирает на время
запроса — сервер перестаёт обслуживать других. Поэтому для async-приложения
берут **async-нативные драйверы**, которые на время ожидания ответа от БД
**отдают управление** циклу:

| БД | Синхронный драйвер | **Async-драйвер (берём его)** |
|---|---|---|
| SQLite | `sqlite3` (стандартный) | **`aiosqlite`** |
| PostgreSQL | `psycopg2` | **`asyncpg`** |

`aiosqlite` — тонкая обёртка над стандартным `sqlite3`: те же курсоры, но каждый
вызов через `await`. `asyncpg` — самостоятельный высокопроизводительный драйвер
Postgres, реализующий его протокол поверх неблокирующих сокетов.

## Параметры запроса — только через плейсхолдеры

Главное правило безопасности: **никогда** не склеивай значения в SQL-строку.

```python
# ОПАСНО — дыра для SQL-инъекции:
await conn.execute(f"SELECT * FROM users WHERE email = '{email}'")

# ПРАВИЛЬНО — значение отдельным аргументом, драйвер сам экранирует:
await conn.execute("SELECT * FROM users WHERE email = $1", email)   # asyncpg
```

Если склеить, злоумышленник передаст `email = "' OR '1'='1"` и прочитает всю
таблицу (или уронит её через `'; DROP TABLE users; --`). Плейсхолдер это исключает.

**Нюанс: синтаксис плейсхолдеров зависит от драйвера.**

| Драйвер | Плейсхолдер | Пример |
|---|---|---|
| `aiosqlite` | `?` | `"... VALUES (?, ?)", (a, b)` |
| `asyncpg` | `$1, $2` | `"... VALUES ($1, $2)", a, b` |

Это классическая боль при переезде с одной БД на другую: приходится
переписывать все запросы. **ORM во второй части урока эту разницу прячет** — ты
пишешь один код, а он генерирует правильный SQL под нужную БД.

## Таймаут на подключение

Postgres — сервер по сети. Попытка подключиться к недоступному серверу без
таймаута **висит**. Задаём предел:

```python
conn = await asyncpg.connect(dsn, timeout=3.0)   # ждём коннект не дольше 3 c
```

Не успели за `timeout` — драйвер бросит исключение, а не зависнет навсегда. В
`02_raw_postgres.py` это обёрнуто в `try/except`: нет сервера — печатаем понятное
сообщение и выходим.

## Пул соединений

Открыть соединение с Postgres дорого (TCP + аутентификация). Держать по
соединению на каждый запрос — расточительно. **Пул** открывает несколько
соединений заранее и выдаёт их по требованию:

```python
pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5, timeout=3.0)
async with pool.acquire() as conn:      # взяли соединение из пула
    rows = await conn.fetch("SELECT ...")
# на выходе из блока соединение вернулось в пул для повторного использования
```

---

# Часть 2. Соединение и сессия

Пара терминов, которые постоянно путают.

- **Соединение (connection)** — открытый канал к БД: по нему летят запросы и
  ответы, внутри него идёт **транзакция**. У сырых драйверов ты работаешь прямо с
  соединением (`conn.execute`, `conn.fetch`).
- **Транзакция** — набор изменений, применяемый «всё или ничего». `commit` фиксирует
  их в БД; `rollback` откатывает. До `commit` изменения видит только твоё соединение.
- **Пул** — набор заранее открытых соединений, которые переиспользуются. `acquire()`
  на время задачи выдаёт одно соединение — это и есть «рабочая сессия» задачи:
  *взял -> поработал -> вернул*.

В ORM (часть 3) поверх соединения появляется свой объект — **`Session`**. Это не
то же самое, что соединение: сессия — «единица работы», которая копит изменения
объектов и переводит их в SQL. Соединение она берёт из пула движка под капотом.

---

# Часть 3. ORM: SQLAlchemy 2.0 (async) + Pydantic

## Зачем ORM

**ORM** (Object-Relational Mapping) отображает **таблицу на класс**, а **строку на
объект**. Вместо строк-кортежей ты получаешь объекты `User`, вместо ручного SQL —
методы. Что это даёт:

- **Объекты вместо кортежей.** `user.email` вместо `row[2]` — читаемо и не сломается
  при добавлении столбца.
- **Один код под разные БД.** ORM сам генерирует SQL нужного диалекта (и правильные
  плейсхолдеры). Переезд SQLite -> Postgres = смена **одной строки URL**.
- **Типизация и связи.** Поля описаны типами, связи между таблицами — атрибутами
  (`user.articles`), а не ручными JOIN.

Цена — надо понимать, что ORM делает под капотом (иначе легко словить лишние
запросы). Поэтому мы и начали с сырого SQL.

## Движок: `create_async_engine`

**Движок (engine)** — центральный объект: он держит **пул соединений**, знает
драйвер и адрес БД. Создаётся один раз на приложение.

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/mydb",
    echo=False,                       # True -> печатать весь генерируемый SQL
    connect_args={"timeout": 5},      # таймаут коннекта -> драйверу asyncpg
    pool_size=5, max_overflow=10,     # параметры пула
)
```

URL кодирует **и диалект, и драйвер**: `диалект+драйвер://...`. Именно смена этой
строки и переключает БД:

| БД | URL движка |
|---|---|
| SQLite (async) | `sqlite+aiosqlite:///demo.db` |
| PostgreSQL (async) | `postgresql+asyncpg://user:pass@host:5432/db` |

## Модель: `DeclarativeBase` + `Mapped`

Модель — это класс-наследник `Base`, поля описаны типизированно (стиль SQLAlchemy 2.0):

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    bio: Mapped[str | None] = mapped_column(String(500))   # | None -> nullable
```

`Mapped[int]` — тип поля в Python; `mapped_column(...)` — как столбец выглядит в БД
(тип, ограничения). `Mapped[str | None]` автоматически делает столбец `NULL`-able.

Создать таблицы по моделям (в async — через `run_sync`, т.к. `create_all` синхронна):

```python
async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
```

> В реальных проектах схему БД не пересоздают, а **мигрируют** инструментом
> **Alembic** (он умеет `ALTER TABLE`, версии, откаты). `create_all` годится для
> уроков, тестов и прототипов — им и пользуемся.

## Сессия как «единица работы»

```python
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session = async_sessionmaker(engine, expire_on_commit=False)

async with async_session() as session:
    session.add(User(name="Иван", email="ivan@example.com"))
    await session.commit()
```

**`Session`** — «единица работы» (unit of work). Ты складываешь в неё объекты и
изменения, а на `commit` она одной транзакцией переводит их в SQL. Что важно
понимать:

- **Identity map.** В пределах одной сессии одна строка БД = один объект в памяти.
  Запросил один и тот же `id` дважды — получишь тот же объект.
- **Автоотслеживание изменений.** Поменял `user.name = "..."` — на `commit` сессия
  сама сгенерирует `UPDATE`. Отдельного «save» не нужно.
- **`flush` vs `commit`.** `flush` шлёт накопленный SQL в БД, но **внутри** текущей
  транзакции (например, чтобы получить сгенерированный `id`); `commit` делает flush
  **и** фиксирует транзакцию. Обычно хватает `commit`.
- **`expire_on_commit=False`.** По умолчанию после `commit` SQLAlchemy помечает поля
  объектов «устаревшими» и при следующем чтении лезет в БД заново. В async это —
  скрытый запрос без `await`, который выстрелит ошибкой. Поэтому для веб-кода ставят
  `expire_on_commit=False`: после `commit` объекты остаются пригодными к чтению.

## CRUD через `select()`

```python
from sqlalchemy import select

# READ: список объектов
result = await session.execute(select(User).where(User.name == "Иван"))
users = result.scalars().all()          # scalars() -> сами объекты, не кортежи
one = result.scalar_one_or_none()       # ровно один объект или None

user = await session.get(User, 1)       # быстрый поиск по первичному ключу

# CREATE
session.add(User(name="Мария", email="maria@example.com"))
await session.commit()

# UPDATE — просто меняем атрибут, unit of work заметит
user.name = "Иван Петров"
await session.commit()

# DELETE
await session.delete(user)
await session.commit()
```

`execute(select(...))` возвращает результат, из которого `scalars()` достаёт
объекты. Частая ошибка новичка — забыть `scalars()` и получить кортежи `(User,)`.

## Async-нюанс: как доставать связанные данные

В синхронном SQLAlchemy можно объявить связь как атрибут и обращаться к нему
(`user.articles`) — ORM **втихую** сходит в БД и подгрузит статьи. В async так
**нельзя**: скрытый запрос без `await` бросает ошибку.

Поэтому в этом уроке связанные таблицы мы соединяем **обычным JOIN'ом** — тем же
приёмом, что в сыром SQL, только запрос собираем через `select().join()`. Это
прозрачно и достаточно для старта (см. часть 4).

> Есть и «продвинутый» путь — объявить связь через `relationship()` и грузить её
> заранее жадной загрузкой (`selectinload`), чтобы ходить по связи как по атрибуту
> (`user.articles`). Это удобнее и решает проблему N+1, но добавляет своих правил.
> Оставим на следующий уровень — сейчас важнее увидеть механизм на JOIN'ах.

## ORM vs Pydantic — та самая связка «ORM Pydantic»

В B2 мы разделяли **модель** (внутренняя сущность) и **схему** (что видит клиент).
Теперь модель — настоящая, из БД, и разделение работает по-крупному:

- **ORM-модель** (`User(Base)`) — как данные лежат в БД, **включая секреты**
  (`password_hash`).
- **Pydantic-схема** (`UserOut(BaseModel)`) — что мы отдаём наружу.

```python
from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # собирать схему из ORM-объекта
    id: int
    name: str
    email: str
    # password_hash здесь НЕТ -> в ответ физически не попадёт

schema = UserOut.model_validate(user)   # user — ORM-объект
schema.model_dump()                     # чистый dict без секретов
```

`from_attributes=True` разрешает `model_validate` читать данные **через атрибуты**
ORM-объекта (`user.email`), а не только из `dict`. Секретное поле не попадёт в
ответ просто потому, что его нет в схеме, — забыть «убрать пароль» невозможно.

Именно это связка «ORM + Pydantic»: **ORM тащит данные из БД, Pydantic формирует
безопасный контракт наружу.** В FastAPI-хендлере это выглядит как
`return UserOut.model_validate(user)` (или `response_model=UserOut`).

---

# Часть 4. Связи между таблицами

Идея всех связей одна: **связь между таблицами — это внешний ключ, а достаём
связанные данные обычным `JOIN`**. Никакой отдельной магии — тот же JOIN, что в
SQL, только через `select().join()`. Держим просто.

## Один-ко-многим: `User` -> `Articles` (файл 04)

У автора много статей, статья принадлежит одному автору. Вся связь — это столбец
**внешнего ключа** `owner_id` в таблице `articles`, ссылающийся на `users.id`:

```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    # Вся связь — вот этот столбец-ключ.
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
```

- **`ForeignKey`** — настоящий столбец в БД: «значение здесь = какой-то `users.id`».
- **`ondelete="CASCADE"`** — удалили пользователя, его статьи удалятся автоматически.

Создаём связь, проставив `owner_id`. Чтобы узнать `id` автора до `commit`, делаем
`flush` — он шлёт `INSERT` и БД присваивает `id`:

```python
ivan = User(name="Иван")
session.add(ivan)
await session.flush()             # теперь ivan.id известен
session.add(Article(title="asyncio", owner_id=ivan.id))
await session.commit()
```

Читаем связанные данные — обычным JOIN по ключу. Результат — строки-кортежи:

```python
result = await session.execute(
    select(User.name, Article.title)
    .join(Article, Article.owner_id == User.id)
)
for name, title in result.all():
    print(name, "->", title)      # Иван -> asyncio
```

## Многие-ко-многим: `Article` <-> `Tag` (файл 05)

У статьи много тегов **и** у тега много статей. Одним внешним ключом это не
выразить — нужна **ассоциативная таблица** (junction table): каждая её строка —
пара `(article_id, tag_id)`, то есть один факт «у этой статьи есть этот тег». Вся
связь = набор таких пар.

Ассоциативную таблицу описывают не моделью, а объектом `Table` (у неё нет своих
данных, только два ключа):

```python
from sqlalchemy import Column, ForeignKey, Table

article_tags = Table(
    "article_tags", Base.metadata,
    Column("article_id", ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
```

Связь = строки-пары, которые мы пишем в эту таблицу явно:

```python
await session.execute(
    article_tags.insert().values([
        {"article_id": a1.id, "tag_id": python.id},
        {"article_id": a1.id, "tag_id": db.id},
    ])
)
await session.commit()
```

Читаем — JOIN уже по трём таблицам (к столбцам `Table` обращаемся через `.c`):

```python
result = await session.execute(
    select(Article.title, Tag.name)
    .join(article_tags, article_tags.c.article_id == Article.id)
    .join(Tag, Tag.id == article_tags.c.tag_id)
)
for title, tag in result.all():
    print(title, "->", tag)
```

## Куда расти дальше

Мы читали связи «в лоб» JOIN'ами — это прозрачно и отлично для старта. У ORM есть и
более удобный (но и более хитрый) слой поверх этого:

- **`relationship()`** — объявляешь связь атрибутом и ходишь по ней как по списку
  объектов (`user.articles`, `article.tags`), без ручных JOIN'ов;
- **жадная загрузка `selectinload`** — обязательна в async, чтобы такую связь
  подгрузить заранее; заодно решает проблему **N+1** (когда на N объектов ORM
  делает N лишних запросов за связанными данными);
- тогда и Pydantic-схема может быть **вложенной** (`UserWithArticles` со списком
  `articles`), и связь уедет в JSON как вложенный массив.

Это следующий уровень — освой сначала JOIN, потом при желании включай `relationship()`.

---

# Часть 5. Как это собрано в боевом проекте

Всё из урока — ровно то, на чём стоит референс-проект
[TestTask_260329](https://github.com/squalusmentor/TestTask_260329) (FastAPI + слои из
B2 + БД, разбирается целиком в B4). Как там разложена БД-часть:

- **`config.py`** — настройки на `pydantic-settings`: параметры БД читаются из
  переменных окружения, а URL собирается свойством:

  ```python
  class Settings(BaseSettings):
      DB_HOST: str = "localhost"; DB_PORT: int = 5432
      DB_USER: str = "postgres"; DB_PASSWORD: str = "postgres"; DB_NAME: str = "app"

      @property
      def database_url(self) -> str:
          return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
  ```

- **`db.py`** — `Base(DeclarativeBase)`, от которого наследуются все модели.
- **`db_connect.py`** — `engine = create_async_engine(...)` и
  `async_session = async_sessionmaker(engine, expire_on_commit=False)`, плюс
  **`connect_with_retry()`**: подключение к БД **несколькими попытками с паузой**.
  Зачем — при старте через Docker Compose приложение поднимается раньше, чем
  Postgres готов принимать соединения; вместо падения делаем `retry` с таймаутом,
  пока БД не ответит.
- **`models/`** — `User` и `Article`, связанные `owner_id` (тот самый
  один-ко-многим из части 4).
- В FastAPI сессию отдают в хендлеры **зависимостью** (`Depends`), чтобы у каждого
  запроса была своя сессия, закрываемая автоматически:

  ```python
  async def get_session():
      async with async_session() as session:
          yield session

  @router.get("/users/{user_id}", response_model=UserOut)
  async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
      user = await session.get(User, user_id)
      ...
  ```

Так замыкается цепочка уроков: **B2** дал слои и `async def`, **B3** насаживает на
слой `services/` настоящую БД — и получается боевой бэкенд.

---

## Практика

Практическое задание — в файле [to-do.md](to-do.md): мини-библиотека
(`Author` -> `Book`, `Book` <-> `Genre`) на async ORM. Пройдёшь своими руками
движок, сессию, CRUD, обе связи и мост в Pydantic.

## Что дальше

Ты умеешь ходить в БД асинхронно — и руками, и через ORM, и связывать таблицы.
Следующие шаги реального бэкенда: **миграции** (Alembic вместо `create_all`),
**авторизация** (JWT, хеш пароля), **пагинация и фильтры** в запросах, **индексы**
для скорости. Всё это навешивается на тот же движок и сессию, что мы разобрали
здесь.
