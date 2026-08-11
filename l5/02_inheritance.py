# Урок L5.2 — Наследование
#
# Наследование выражает связь "является" (IS-A): Book ЯВЛЯЕТСЯ Item.
# Подкласс получает атрибуты и методы родителя и может их дополнять или
# переопределять. Цель — переиспользовать общее, не копируя код.


class Item:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity

    def label(self) -> str:
        return f"{self.name} ({self.quantity} шт.)"

    def kind(self) -> str:
        return "предмет"


# Подкласс: class Подкласс(Родитель)
class Book(Item):
    def __init__(self, name: str, quantity: int, author: str):
        # super() вызывает родителя — не дублируем его __init__ руками.
        super().__init__(name, quantity)
        self.author = author              # своё поле

    # Переопределяем (override) метод родителя.
    def label(self) -> str:
        base = super().label()            # можно дополнить родительскую версию
        return f"{base}, автор: {self.author}"

    def kind(self) -> str:
        return "книга"


class Tool(Item):
    def __init__(self, name, quantity, condition="новый"):
        super().__init__(name, quantity)
        self.condition = condition

    def kind(self) -> str:
        return "инструмент"
    # label() НЕ переопределён — используется родительский.


def demo2():
    print("-- подкласс получает поведение родителя --")
    book = Book("Чистый код", 3, "Роберт Мартин")
    tool = Tool("Дрель", 2, condition="б/у")
    print("  book.label() =", book.label())   # переопределён
    print("  tool.label() =", tool.label())   # унаследован от Item
    print("  book.kind() =", book.kind(), "| tool.kind() =", tool.kind())

    print("-- проверки родства --")
    print("  isinstance(book, Book) =", isinstance(book, Book))
    print("  isinstance(book, Item) =", isinstance(book, Item))   # книга — это и Item
    print("  isinstance(tool, Book) =", isinstance(tool, Book))   # False
    print("  issubclass(Book, Item) =", issubclass(Book, Item))

    print("-- общий список разнородных объектов --")
    items = [book, tool, Item("Скрепка", 1000)]
    for it in items:
        print(f"  [{it.kind()}] {it.label()}")


if __name__ == "__main__":
    demo2()
