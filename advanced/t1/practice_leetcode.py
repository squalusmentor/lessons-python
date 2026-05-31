"""
ПРАКТИКА 2 — Пара простых задач с LeetCode (на циклы).

Реализуй функции ниже, затем запусти:

    python practice_leetcode.py

Эталон: solutions/practice_leetcode_solution.py
"""


def fizz_buzz(n):
    """LeetCode 412. Вернуть список строк от 1 до n:
    кратно 3 -> "Fizz", кратно 5 -> "Buzz", кратно 15 -> "FizzBuzz",
    иначе само число строкой.
    fizz_buzz(5) -> ['1', '2', 'Fizz', '4', 'Buzz']"""
    pass  # TODO


def running_sum(nums):
    """LeetCode 1480. Вернуть список нарастающих сумм:
    каждый элемент — сумма всех предыдущих включительно.
    running_sum([1, 2, 3, 4]) -> [1, 3, 6, 10]"""
    pass  # TODO


# ── простой self-check ──────────────────────────────────────────────────────

def _check(name, got, expected):
    mark = "OK  " if got == expected else "FAIL"
    print(f"[{mark}] {name}")
    if got != expected:
        print(f"       ожидалось: {expected!r}")
        print(f"       получено:  {got!r}")


if __name__ == "__main__":
    _check("fizz_buzz(5)", fizz_buzz(5), ["1", "2", "Fizz", "4", "Buzz"])
    _check("fizz_buzz(15)[-1]", fizz_buzz(15)[-1] if fizz_buzz(15) else None,
           "FizzBuzz")
    _check("running_sum([1,2,3,4])", running_sum([1, 2, 3, 4]), [1, 3, 6, 10])
    _check("running_sum([])", running_sum([]), [])
