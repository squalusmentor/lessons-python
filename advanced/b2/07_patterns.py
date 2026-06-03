# Урок B2.7 — Паттерны и методы класса
#
# Паттерн — типовое решение типовой задачи. Здесь: ФАБРИКА (гибкое создание
# объектов) и СИНГЛТОН (единственный экземпляр). Заодно разберём @classmethod
# и @staticmethod — это всё ещё декораторы (привет из B1), но навешенные на методы.


class Item:
    count = 0   # счётчик созданных (атрибут КЛАССА)

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        Item.count += 1

    # classmethod получает сам КЛАСС (cls), а не экземпляр.
    # Классическое применение — ФАБРИКА (альтернативный конструктор).
    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(data["name"], data["quantity"])

    # staticmethod не получает ни self, ни cls — просто функция в неймспейсе класса.
    @staticmethod
    def is_valid_name(name: str) -> bool:
        return bool(name) and name.strip() == name

    def __repr__(self):
        return f"Item({self.name!r}, {self.quantity})"


# --- Синглтон через __new__: класс всегда возвращает ОДИН и тот же объект ---
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.settings = {}   # инициализируем ровно один раз
        return cls._instance


# --- Синглтон через декоратор (замыкание из B1 в деле) ---
def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    def __init__(self):
        self.lines = []


def demo7():
    print("-- фабрика: classmethod как альтернативный конструктор --")
    data = {"name": "Отвёртка", "quantity": 7}
    it = Item.from_dict(data)     # из словаря (привет из B1: dict -> объект)
    print("  Item.from_dict(...) =", it)

    print("-- staticmethod: утилита без self/cls --")
    print("  is_valid_name('Болт') =", Item.is_valid_name("Болт"))
    print("  is_valid_name(' Болт ') =", Item.is_valid_name(" Болт "))

    print("-- атрибут класса как общий счётчик --")
    print("  всего создано Item.count =", Item.count)

    print("-- синглтон через __new__ --")
    a = Config()
    b = Config()
    a.settings["debug"] = True
    print("  a is b:", a is b)             # один и тот же объект
    print("  b.settings:", b.settings)     # изменение видно через b

    print("-- синглтон через декоратор --")
    l1 = Logger()
    l2 = Logger()
    print("  l1 is l2:", l1 is l2)

    print("-- почему синглтон ОСТОРОЖНО --")
    print("  плюс: один общий ресурс (конфиг, пул соединений, лог).")
    print("  минус: скрытое глобальное состояние, трудно тестировать.")
    print("  часто чище просто СОЗДАТЬ объект один раз и ПЕРЕДАТЬ его, куда нужно.")


if __name__ == "__main__":
    demo7()
