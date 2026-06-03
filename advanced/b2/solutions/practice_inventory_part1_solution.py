"""
Урок B2 — РЕШЕНИЕ практической работы, ЧАСТЬ 1 (классы предметов).
Самодостаточный файл: python solutions/practice_inventory_part1_solution.py
"""


class Item:
    def __init__(self, item_id: str, name: str, quantity: int):
        self.item_id = item_id
        self.name = name
        if quantity < 0:
            raise ValueError("количество не может быть отрицательным")
        self._quantity = quantity        # инкапсуляция: меняем только методами

    @property
    def quantity(self) -> int:
        return self._quantity

    def restock(self, n: int) -> None:
        if n <= 0:
            raise ValueError("добавлять можно только положительное количество")
        self._quantity += n

    def take(self, n: int) -> None:
        if n <= 0:
            raise ValueError("забирать можно только положительное количество")
        if n > self._quantity:
            raise ValueError(f"на складе только {self._quantity}, нельзя забрать {n}")
        self._quantity -= n

    def label(self) -> str:
        return f"[{self.item_id}] {self.name} — {self._quantity} шт."

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.item_id!r}, {self.name!r}, {self._quantity})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.item_id == other.item_id

    def __hash__(self) -> int:
        return hash(self.item_id)

    def __lt__(self, other) -> bool:
        return self.name < other.name


class Book(Item):
    def __init__(self, item_id, name, quantity, author):
        super().__init__(item_id, name, quantity)
        self.author = author

    def label(self) -> str:
        return super().label() + f", автор: {self.author}"


class Tool(Item):
    def __init__(self, item_id, name, quantity, condition="новый"):
        super().__init__(item_id, name, quantity)
        self.condition = condition

    def label(self) -> str:
        return super().label() + f", состояние: {self.condition}"


def print_catalog(items) -> None:
    for it in items:
        print("  " + it.label())


def demo():
    print("== РЕШЕНИЕ части 1: классы предметов ==")
    hammer = Tool("A-1", "Молоток", 5)
    book = Book("B-1", "Чистый код", 3, author="Роберт Мартин")
    clip = Item("C-1", "Скрепка", 1000)

    print("-- label() полиморфен --")
    print_catalog([hammer, book, clip])

    print("-- инкапсуляция: инвариант склада --")
    hammer.take(2)
    print("  после take(2):", hammer.label())
    try:
        hammer.take(100)
    except ValueError as e:
        print("  поймали:", e)

    print("-- dunder: ==, hash, сортировка --")
    print("  равенство по item_id:", book == Book("B-1", "x", 0, "y"))
    # дубль с тем же id схлопнется в множестве (равны по item_id и hash совпал):
    print("  set без дублей по id:", {hammer, book, clip, Tool("A-1", "дубль", 1)})
    print("  sorted по имени:", [it.name for it in sorted([hammer, book, clip])])


if __name__ == "__main__":
    demo()
