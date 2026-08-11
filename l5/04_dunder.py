# Урок L5.4 — Dunder-методы (магические, __double_underscore__)
#
# Dunder-методы подключают твой объект к синтаксису и встроенным функциям языка:
# print(), ==, <, +, len(), in, []. Python вызывает их за тебя в нужный момент.


class Money:
    def __init__(self, amount: int, currency: str = "RUB"):
        self.amount = amount
        self.currency = currency

    # __repr__ — для РАЗРАБОТЧИКА (отладка, REPL). Желательно однозначно.
    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"

    # __str__ — для ЧЕЛОВЕКА (print, str()). Нет __str__ -> берётся __repr__.
    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    # __eq__ — оператор ==
    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)

    # Определил __eq__ — определи и __hash__, иначе объект станет нехешируемым
    # (его нельзя будет класть в set или использовать ключом dict).
    def __hash__(self) -> int:
        return hash((self.amount, self.currency))

    # __lt__ — оператор < ; даёт работу sorted(), min(), max().
    def __lt__(self, other) -> bool:
        return self.amount < other.amount

    # __add__ — оператор + (перегрузка оператора).
    def __add__(self, other) -> "Money":
        if self.currency != other.currency:
            raise ValueError("разные валюты не складываем")
        return Money(self.amount + other.amount, self.currency)


class Bag:
    """Контейнерные dunder: __len__, __contains__, __getitem__."""

    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __contains__(self, x):
        return x in self._items

    def __getitem__(self, i):
        return self._items[i]


def demo4():
    print("-- __repr__ против __str__ --")
    m = Money(100)
    print("  str(m) =", str(m))     # для человека
    print("  repr(m) =", repr(m))   # для отладки
    print("  print(m):", m)         # print зовёт __str__

    print("-- == и хеш --")
    print("  Money(100) == Money(100):", Money(100) == Money(100))
    print("  множество схлопывает дубли:", {Money(100), Money(100), Money(50)})

    print("-- сортировка через __lt__ --")
    wallet = [Money(300), Money(50), Money(150)]
    print("  sorted:", sorted(wallet))
    print("  max:", max(wallet))

    print("-- перегрузка оператора + --")
    print("  Money(100) + Money(50) =", Money(100) + Money(50))

    print("-- контейнерные dunder: len / in / [] --")
    bag = Bag(["a", "b", "c"])
    print("  len(bag) =", len(bag))
    print("  'b' in bag =", "b" in bag)
    print("  bag[0] =", bag[0])
    print("  итерация (через __getitem__):", [x for x in bag])


if __name__ == "__main__":
    demo4()
