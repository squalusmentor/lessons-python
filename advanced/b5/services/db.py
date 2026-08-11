from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Общий предок всех моделей. Хранит metadata — реестр таблиц.

    Живёт в отдельном модуле, чтобы модели импортировали только его и не
    тянули за собой движок (иначе получился бы circular import:
    db_connect -> models -> db_connect).
    """
