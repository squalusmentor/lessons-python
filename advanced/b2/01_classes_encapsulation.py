# Урок B2.1 — Классы и инкапсуляция
#
# Класс — это "чертёж" объекта: данные (атрибуты) и поведение (методы) в одном
# месте. Объект (экземпляр) создаётся вызовом класса: obj = MyClass(...).
# ООП нужно не ради синтаксиса, а чтобы СВЯЗАТЬ данные с их инвариантами.


class Product:
    """Товар на складе. Показывает атрибуты, методы и инкапсуляцию."""

    # Атрибут КЛАССА — один на всех, общий для всех экземпляров.
    category = "товар"

    def __init__(self, name: str, quantity: int):
        # self — это сам создаваемый объект. Атрибуты ЭКЗЕМПЛЯРА живут в self.
        self.name = name                 # публичный атрибут
        self._quantity = quantity        # _одно: "снаружи не трогай" (договорённость)
        self.__secret_code = "SKU-000"   # __два: name mangling -> _Product__secret_code

    # Обычный метод: первым параметром ВСЕГДА self.
    def restock(self, n: int) -> None:
        if n <= 0:
            raise ValueError("добавлять можно только положительное количество")
        self._quantity += n

    def take(self, n: int) -> None:
        # Инкапсуляция ради ДЕЛА: метод хранит инвариант "склад не уходит в минус".
        if n > self._quantity:
            raise ValueError(f"на складе только {self._quantity}, нельзя забрать {n}")
        self._quantity -= n

    def info(self) -> str:
        return f"{self.name}: {self._quantity} шт."


def demo1():
    print("-- создание объекта --")
    p = Product("Молоток", 5)
    print("  p.name =", p.name)
    print("  p.category =", p.category)   # атрибут класса виден через экземпляр
    print("  p.info() =", p.info())

    print("-- методы хранят инвариант --")
    p.restock(10)
    p.take(3)
    print("  после +10 и -3:", p.info())
    try:
        p.take(100)
    except ValueError as e:
        print("  поймали:", e)

    print("-- уровни доступа: это сигналы, а не замки --")
    # Python НЕ запрещает доступ. Подчёркивания — соглашение, а не приватность.
    print("  p._quantity (можно, но не нужно):", p._quantity)
    # p.__secret_code -> AttributeError: имя "исковеркано" name mangling-ом
    print("  настоящее имя __secret_code:", p._Product__secret_code)

    print("-- атрибут класса против атрибута экземпляра --")
    a = Product("A", 1)
    b = Product("B", 1)
    Product.category = "инвентарь"        # меняем у класса -> видят все
    print("  a.category =", a.category, "| b.category =", b.category)
    a.category = "личное"                 # создаём атрибут ЭКЗЕМПЛЯРА (тень)
    print("  a.category =", a.category, "| b.category =", b.category)


if __name__ == "__main__":
    demo1()
