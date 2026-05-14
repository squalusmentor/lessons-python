# Урок 2.3 — Функции: параметры, type hints, *args/**kwargs, lambda, замыкания, рекурсия


# Простая функция. Type hints необязательны, но в реальных проектах их пишут.
def add(a: int, b: int) -> int:
    return a + b


# Значение параметра по умолчанию.
# ВНИМАНИЕ: дефолт вычисляется один раз при объявлении.
# Поэтому изменяемые объекты ([], {}) дефолтом ставить нельзя — используй None.
def greet(name: str, greeting: str = "Привет") -> None:
    print(f"{greeting}, {name}!")


# Возврат "нескольких значений" — на самом деле возврат кортежа.
# При вызове его сразу распаковывают: q, r = divmod_(...).
def divmod_(a: int, b: int) -> tuple[int, int]:
    return a // b, a % b


# Ошибки в Python — через исключения
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("деление на ноль")
    return a / b


# *args — собирает оставшиеся ПОЗИЦИОННЫЕ аргументы в кортеж.
def total(*nums: int) -> int:
    s = 0
    for n in nums:
        s += n
    return s


# **kwargs — собирает оставшиеся ИМЕНОВАННЫЕ аргументы в словарь.
def describe(**fields):
    for key, value in fields.items():
        print(f"  {key} = {value}")


# Рекурсия. База — n <= 1.
# Помни про лимит глубины (~1000)
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


# Функция, возвращающая функцию
# x захвачен из внешней функции и живёт вместе с inner.
# декораторы - основываются на этом - популярный паттерн
def multiplier(x: int):
    def inner(y: int) -> int:
        return x * y
    return inner


def demo3():

    # === Простой вызов ===
    print("add(3, 4) =", add(3, 4))

    # === Аргументы по умолчанию + именованные аргументы ===
    greet("Аня")
    greet("Боря", greeting="Здравствуй")
    greet(greeting="Хай", name="Вика")  # порядок не важен, если по имени

    # === Кортеж как "несколько возвращаемых значений" ===
    q, r = divmod_(17, 5)
    print(f"17 / 5 = {q} ост {r}")

    # === Ошибка через исключение ===
    try:
        print(divide(10, 3))
        print(divide(1, 0))
    except ValueError as e:
        print("ошибка:", e)

    # === *args ===
    print("total(1,2,3) =", total(1, 2, 3))
    print("total(10,20,30,40) =", total(10, 20, 30, 40))

    # Распаковка списка в *args через *
    nums = [1, 2, 3, 4, 5]
    print("total(*nums) =", total(*nums))

    # === **kwargs ===
    print("describe(...):")
    describe(name="Аня", age=25, city="Москва")

    # === Рекурсия ===
    print("5! =", factorial(5))

    # === Функция — это значение ===
    op = add
    print("op(2, 3) =", op(2, 3))

    # === Замыкание ===
    double = multiplier(2)
    triple = multiplier(3)
    print("double(5) =", double(5))
    print("triple(5) =", triple(5))

    # === lambda — анонимная функция ===
    square = lambda x: x * x
    print("square(5) =", square(5))

    # Типичное применение — передать как аргумент в sorted/map/filter
    pairs = [("Аня", 30), ("Боря", 25), ("Вика", 28)]
    pairs.sort(key=lambda p: p[1])
    print("сортировка по возрасту:", pairs)


if __name__ == "__main__":
    demo3()
