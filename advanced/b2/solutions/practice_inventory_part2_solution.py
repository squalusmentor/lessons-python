"""
Урок B2 — РЕШЕНИЕ практической работы, ЧАСТЬ 2 (менеджер инвентаря).
Самодостаточный файл: python solutions/practice_inventory_part2_solution.py

Темы: property (валидируемое quantity), композиция (Inventory содержит предметы),
паттерны (Warehouse — синглтон, Item.from_dict — фабрика), простой CLI.
"""


# --- Классы предметов: количество защищено property ---
class Item:
    def __init__(self, item_id, name, quantity):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity            # через сеттер property

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("количество не может быть отрицательным")
        self._quantity = value

    # ФАБРИКА: выбирает класс по полю "type".
    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        kind = data.get("type", "item")
        if kind == "book":
            return Book(data["item_id"], data["name"], data["quantity"], data["author"])
        if kind == "tool":
            return Tool(data["item_id"], data["name"], data["quantity"],
                        data.get("condition", "новый"))
        return Item(data["item_id"], data["name"], data["quantity"])

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


# --- КОМПОЗИЦИЯ: Inventory СОДЕРЖИТ предметы (а не наследует dict) ---
class Inventory:
    def __init__(self):
        self._items = {}                    # item_id -> Item

    def add(self, item: Item) -> None:
        existing = self._items.get(item.item_id)
        if existing is None:
            self._items[item.item_id] = item
        else:
            existing.quantity += item.quantity   # дозаказ того же артикула

    def find(self, query: str):
        q = query.lower()
        return [it for it in self._items.values() if q in it.name.lower()]

    def issue(self, item_id: str, n: int) -> None:
        if item_id not in self._items:
            raise KeyError(f"нет предмета с id {item_id}")
        if n <= 0:
            raise ValueError("выдавать нужно положительное количество")
        self._items[item_id].quantity -= n      # property не пустит ниже нуля

    @property
    def total_quantity(self) -> int:
        return sum(it.quantity for it in self._items.values())

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def __contains__(self, item_id):
        return item_id in self._items


# --- СИНГЛТОН: единственный общий склад на всё приложение ---
class Warehouse:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.inventory = Inventory()
        return cls._instance


def run_cli() -> None:
    inv = Warehouse().inventory
    print("Команды: add <id> <name> <qty> | find <text> | issue <id> <qty> | list | quit")
    while True:
        try:
            raw = input("> ").strip()
        except EOFError:
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0]
        try:
            if cmd == "quit":
                break
            elif cmd == "add":
                _, item_id, name, qty = parts
                inv.add(Item(item_id, name, int(qty)))
                print(f"  добавлено: {item_id}")
            elif cmd == "find":
                found = inv.find(parts[1])
                for it in found:
                    print("  " + it.label())
                if not found:
                    print("  ничего не найдено")
            elif cmd == "issue":
                _, item_id, qty = parts
                inv.issue(item_id, int(qty))
                print(f"  выдано {qty} шт. ({item_id})")
            elif cmd == "list":
                for it in sorted(inv, key=lambda x: x.name):
                    print("  " + it.label())
                print(f"  всего штук: {inv.total_quantity}")
            else:
                print("  неизвестная команда")
        except (ValueError, KeyError) as e:
            print("  ошибка:", e)


def demo():
    print("== РЕШЕНИЕ части 2: менеджер инвентаря (скриптовый сценарий) ==")
    wh = Warehouse()
    wh.inventory.add(Item.from_dict({"type": "tool", "item_id": "A-1",
                                     "name": "Дрель", "quantity": 2}))
    wh.inventory.add(Item.from_dict({"type": "book", "item_id": "B-1",
                                     "name": "Чистый код", "quantity": 3,
                                     "author": "Роберт Мартин"}))
    wh.inventory.add(Item.from_dict({"type": "item", "item_id": "C-1",
                                     "name": "Скрепка", "quantity": 1000}))
    print("  разных предметов:", len(wh.inventory))
    print("  всего штук:", wh.inventory.total_quantity)

    print("-- синглтон: другой Warehouse() видит те же данные --")
    print("  Warehouse() is wh:", Warehouse() is wh)
    print("  поиск 'код':", [it.label() for it in Warehouse().inventory.find("код")])

    print("-- выдача (property держит инвариант) --")
    wh.inventory.issue("A-1", 1)
    print("  после выдачи 1 дрели, всего штук:", wh.inventory.total_quantity)
    try:
        wh.inventory.issue("A-1", 100)
    except ValueError as e:
        print("  поймали:", e)

    print("-- интерактивный режим: раскомментируй run_cli() ниже --")
    # run_cli()


if __name__ == "__main__":
    demo()
