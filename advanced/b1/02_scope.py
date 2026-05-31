# Урок B1.2 — Область видимости: правило LEGB, global, nonlocal
#
# Python ищет имя по правилу LEGB, именно в этом порядке:
#   Local     — локальные имена функции
#   Enclosing — имена объемлющей функции (для вложенных)
#   Global    — имена уровня модуля
#   Built-in  — встроенные (len, print, range, ...)
# Нашёл — остановился. Не нашёл нигде — NameError.


counter = 0  # глобальное имя уровня модуля


def read_global() -> None:
    # ЧИТАТЬ глобальное можно без объявлений.
    print(f"  вижу counter = {counter}")


def try_change_wrong() -> None:
    # ПРИСВАИВАНИЕ создаёт ЛОКАЛЬНУЮ переменную — глобальную не трогает.
    counter = 999
    print(f"  локальный counter = {counter}")


def change_global() -> None:
    global counter   # теперь присваивание идёт в ГЛОБАЛЬНУЮ
    counter += 1


def broken() -> None:
    # Классическая ловушка: из-за присваивания НИЖЕ имя x стало локальным
    # во всей функции, поэтому строка-чтение падает с UnboundLocalError.
    try:
        print(x)     # ещё не присвоено, но имя уже локальное → ошибка
        x = 1
    except UnboundLocalError as e:
        print("  UnboundLocalError:", e)


def shadow_builtin() -> None:
    # Тень над встроенным именем: list здесь — локальная переменная, не тип.
    list = [3, 1, 2]   # перекрыли встроенный list
    print("  list =", list)
    # list((1, 2))  # тут уже TypeError — встроенный list недоступен


def demo2():
    print("-- читаем глобальное --")
    read_global()

    print("-- присваивание создаёт локальную --")
    try_change_wrong()
    print(f"  глобальный counter НЕ изменился: {counter}")

    print("-- global: меняем глобальное --")
    change_global()
    change_global()
    print(f"  теперь counter = {counter}")

    print("-- UnboundLocalError --")
    broken()

    print("-- тень над встроенным (так делать не надо) --")
    shadow_builtin()

    print("-- область видимости у comprehension --")
    # Переменная цикла внутри comprehension НЕ утекает наружу (в отличие от for).
    squares = [i * i for i in range(3)]
    print("  squares =", squares)
    # print(i)  # NameError: i не существует снаружи comprehension


if __name__ == "__main__":
    demo2()
