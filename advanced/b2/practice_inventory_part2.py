"""
Урок B2 — ПРАКТИЧЕСКАЯ РАБОТА, ЧАСТЬ 2 (Занятие 2: property, композиция vs
наследование, паттерны).

Продолжаем CLI-менеджер инвентаря. Классы предметов из части 1 даны ниже
ГОТОВЫМИ — но количество усилено через property: теперь склад нельзя увести
в минус даже прямым присваиванием quantity. Твоя задача — собрать МЕНЕДЖЕР:

  - Inventory       — хранилище через КОМПОЗИЦИЮ (содержит предметы, а не наследует);
  - Warehouse       — СИНГЛТОН: единственный общий склад на всё приложение;
  - Item.from_dict  — ФАБРИКА: создание нужного подкласса из словаря (команда -> объект);
  - run_cli()       — простой цикл команд: add / find / issue / list / quit.

Запуск:  python practice_inventory_part2.py
Решение: solutions/practice_inventory_part2_solution.py
"""


# =====================================================================
# --- ДАНО: классы предметов из части 1 (количество через property) ---
# =====================================================================
class Item:
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity            # пойдёт через сеттер property

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("количество не может быть отрицательным")
        self._quantity = value

    # ФАБРИКА (TODO 3 — допиши тело).
    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        raise NotImplementedError("TODO 3: создать нужный класс по data['type']")

    def label(self):
        return f"[{self.item_id}] {self.name} — {self.quantity} шт."

    def __repr__(self):
        return f"{type(self).__name__}({self.item_id!r}, {self.name!r}, {self.quantity})"


class Book(Item):
    def __init__(self, item_id, name, quantity, author):
        super().__init__(item_id, name, quantity)
        self.author = author

    def label(self):
        return super().label() + f", автор: {self.author}"


class Tool(Item):
    def __init__(self, item_id, name, quantity, condition="новый"):
        super().__init__(item_id, name, quantity)
        self.condition = condition

    def label(self):
        return super().label() + f", состояние: {self.condition}"


# =====================================================================
# === TODO 1. Inventory — КОМПОЗИЦИЯ ===
# Inventory СОДЕРЖИТ предметы (dict item_id -> Item), а НЕ наследует dict/list.
# Методы:
#   add(item)           — положить предмет; если item_id уже есть — сложить количество
#   find(query)         — список предметов, у кого query входит в name (без регистра)
#   issue(item_id, n)   — ВЫДАЧА: уменьшить количество на n; нет такого id -> KeyError.
#                         Само уменьшение делай через item.quantity -= n —
#                         property не пустит ниже нуля (поднимет ValueError).
#   total_quantity      — @property: сумма quantity всех предметов (вычисляемое)
#   __len__             — сколько РАЗНЫХ предметов
#   __iter__            — перебор предметов (for it in inventory)
#   __contains__        — item_id in inventory
#
# class Inventory:
#     def __init__(self):
#         self._items = {}
#     ...
# =====================================================================


# =====================================================================
# === TODO 2. Warehouse — СИНГЛТОН ===
# Единственный общий склад. Warehouse() всегда возвращает один и тот же объект,
# внутри которого один Inventory (доступ: warehouse.inventory).
# Подсказка: __new__ + классовый атрибут _instance (см. 07_patterns.py, Config).
#
# class Warehouse:
#     ...
# =====================================================================


# =====================================================================
# === TODO 3. Item.from_dict (фабрика) — допиши метод выше ===
# По полю data["type"]:
#   "book" -> Book(item_id, name, quantity, author)
#   "tool" -> Tool(item_id, name, quantity, condition)  (condition по умолчанию "новый")
#   иначе  -> Item(item_id, name, quantity)
# Пример словаря: {"type": "tool", "item_id": "A-1", "name": "Дрель", "quantity": 2}
# =====================================================================


# =====================================================================
# === TODO 4. run_cli() — простой цикл команд ===
# Читай input(), разбивай по пробелам. Команды:
#   add <id> <name> <qty>   — добавить простой Item
#   find <text>             — найти по подстроке имени
#   issue <id> <qty>        — выдать со склада
#   list                    — показать каталог и общее количество
#   quit                    — выход
# Склад бери через Warehouse().inventory (синглтон -> один на всех).
# Лови ValueError/KeyError и печатай понятную ошибку, НЕ роняя цикл.
#
# def run_cli() -> None:
#     ...
# =====================================================================


def demo():
    print("== Часть 2: менеджер инвентаря (скриптовый сценарий) ==")
    # Раскомментируй блоки по мере выполнения TODO.

    # wh = Warehouse()
    # wh.inventory.add(Item.from_dict({"type": "tool", "item_id": "A-1",
    #                                  "name": "Дрель", "quantity": 2}))
    # wh.inventory.add(Item.from_dict({"type": "book", "item_id": "B-1",
    #                                  "name": "Чистый код", "quantity": 3,
    #                                  "author": "Роберт Мартин"}))
    # print("  разных предметов:", len(wh.inventory))
    # print("  всего штук:", wh.inventory.total_quantity)

    # print("-- синглтон: другой Warehouse() видит те же данные --")
    # print("  Warehouse() is wh:", Warehouse() is wh)
    # print("  поиск 'код':", [it.label() for it in Warehouse().inventory.find("код")])

    # print("-- выдача --")
    # wh.inventory.issue("A-1", 1)
    # print("  после выдачи 1 дрели, всего штук:", wh.inventory.total_quantity)

    # Для интерактивного режима раскомментируй:
    # run_cli()


if __name__ == "__main__":
    demo()
