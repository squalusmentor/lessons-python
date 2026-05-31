# Урок B1.5 — Рекурсия
#
# Любая корректная рекурсия = БАЗА (выход без вызова себя) + ШАГ (вызов себя
# на меньшей задаче, приближающий к базе).
import sys
from functools import lru_cache


def factorial(n: int) -> int:
    if n <= 1:                      # база
        return 1
    return n * factorial(n - 1)     # шаг


# Наивные числа Фибоначчи: красиво, но ЭКСПОНЕНЦИАЛЬНО медленно —
# одно и то же значение пересчитывается множество раз (двойная рекурсия).
def fib_naive(n: int) -> int:
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# Та же рекурсия + мемоизация: lru_cache кэширует результат по аргументам.
@lru_cache(maxsize=None)
def fib_fast(n: int) -> int:
    if n < 2:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)


# Рекурсия особенно естественна для ВЛОЖЕННЫХ структур неизвестной глубины.
def deep_sum(data: list) -> int:
    total = 0
    for item in data:
        if isinstance(item, list):
            total += deep_sum(item)   # элемент — список → углубляемся
        else:
            total += item
    return total


def demo5():
    print("-- факториал --")
    print("  5! =", factorial(5))
    print("  10! =", factorial(10))

    print("-- Фибоначчи: наивный против мемоизации --")
    print("  fib_naive(10) =", fib_naive(10))
    print("  fib_fast(100) =", fib_fast(100))   # мгновенно; наивный тут зависнет

    print("-- сумма вложенного списка --")
    print("  deep_sum([1, [2, 3, [4, 5]], 6]) =", deep_sum([1, [2, 3, [4, 5]], 6]))

    print("-- лимит глубины рекурсии --")
    print("  sys.getrecursionlimit() =", sys.getrecursionlimit())

    # В Python НЕТ хвостовой оптимизации: рекурсия без базы упрётся в лимит.
    def runaway(n):
        return runaway(n + 1)   # нет базы → RecursionError
    try:
        runaway(0)
    except RecursionError:
        print("  поймали RecursionError (нет базы) — глубокую рекурсию пишут итеративно")


if __name__ == "__main__":
    demo5()
