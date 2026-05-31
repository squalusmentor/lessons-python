# Урок B1.4 — Функции как объекты первого класса
#
# Функция в Python — обычный объект: её можно положить в переменную, передать
# аргументом, вернуть из другой функции, сложить в список/словарь, навесить атрибут.
from functools import reduce


def add(a, b):
    """Сложение."""
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


# Функция высшего порядка: принимает другую функцию как аргумент.
def apply_twice(func, x):
    return func(func(x))


# Таблица диспетчеризации: словарь "имя -> функция" вместо длинной цепочки if/elif.
OPERATIONS = {"+": add, "-": sub, "*": mul}


def calc(a, op, b):
    func = OPERATIONS[op]   # достаём функцию по ключу
    return func(a, b)


def demo4():
    print("-- функция это значение --")
    f = add            # без скобок — берём саму функцию, не вызываем
    print("  f(2, 3) =", f(2, 3))
    print("  f.__name__ =", f.__name__)

    print("-- функция как аргумент (higher-order) --")
    print("  apply_twice(x+1, 10) =", apply_twice(lambda x: x + 1, 10))

    print("-- таблица диспетчеризации --")
    print("  calc(6, '+', 4) =", calc(6, "+", 4))
    print("  calc(6, '*', 4) =", calc(6, "*", 4))

    print("-- встроенные higher-order: map / filter / sorted --")
    nums = [5, 2, 8, 1, 9, 3]
    print("  map (квадраты):", list(map(lambda x: x * x, nums)))
    print("  filter (чётные):", list(filter(lambda x: x % 2 == 0, nums)))
    print("  sorted (по убыв.):", sorted(nums, reverse=True))

    words = ["banana", "kiwi", "apple", "fig"]
    print("  sorted по длине:", sorted(words, key=len))
    print("  sorted по последней букве:", sorted(words, key=lambda w: w[-1]))

    print("-- functools.reduce: свернуть список в одно значение --")
    print("  произведение:", reduce(mul, nums))   # mul применяется по цепочке

    print("-- у функции есть атрибуты (она объект) --")
    add.calls = 0        # функциям можно навешивать свои атрибуты
    print("  add.calls =", add.calls)
    print("  add.__doc__ =", add.__doc__)


if __name__ == "__main__":
    demo4()
