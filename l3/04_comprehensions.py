# Урок L3.4 — Генераторы списков (list comprehension)


def demo4():

    # === Было: обычный цикл с append ===
    print("-- обычный цикл --")
    squares = []
    for n in range(1, 6):
        squares.append(n ** 2)
    print(squares)

    # === Стало: list comprehension ===
    print("-- list comprehension --")
    squares = [n ** 2 for n in range(1, 6)]
    print(squares)

    # === С фильтром if ===
    print("-- с фильтром --")
    evens = [n for n in range(1, 11) if n % 2 == 0]
    print(evens)

    # === С преобразованием элементов ===
    print("-- с преобразованием --")
    names = ["аня", "боря", "вика"]
    print([name.capitalize() for name in names])

    # === Условие-выбор внутри выражения (тернарник) ===
    print("-- тернарник внутри --")
    print(["чёт" if n % 2 == 0 else "нечёт" for n in range(5)])


if __name__ == "__main__":
    demo4()
