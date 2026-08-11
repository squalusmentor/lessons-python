# Урок L4.6 — ЗАДАЧИ НА РЕКУРСИЮ
#
# Как пользоваться:
#   1. Раскомментируй задание (функцию).
#   2. Реализуй ТОЛЬКО через рекурсию (без for/while).
#   3. В demo6() раскомментируй проверки и запусти: python 06_recursion_tasks.py
#
# Каждая задача — это БАЗА + ШАГ. Сначала найди базу (самый маленький вход),
# потом шаг (как свести задачу к чуть меньшей).
#
# Решения — в solutions/recursion_tasks_solution.py (подглядывай после попытки).


# === 1. sum_to ===
# Сумма чисел от 1 до n.
#   sum_to(5) -> 15   (1+2+3+4+5)
#   sum_to(1) -> 1
# База: n == 1. Шаг: n + sum_to(n - 1).
#
# def sum_to(n: int) -> int:
#     ...


# === 2. count_digits ===
# Сколько цифр в неотрицательном числе. Без str().
#   count_digits(0)     -> 1
#   count_digits(7)     -> 1
#   count_digits(12345) -> 5
# Подсказка: n // 10 убирает последнюю цифру; база — n < 10.
#
# def count_digits(n: int) -> int:
#     ...


# === 3. reverse_string ===
# Перевернуть строку рекурсивно (без [::-1]).
#   reverse_string("abc") -> "cba"
#   reverse_string("")    -> ""
# Подсказка: reverse(s[1:]) + s[0].
#
# def reverse_string(s: str) -> str:
#     ...


# === 4. power ===
# Возвести base в неотрицательную степень exp. Без ** и pow().
#   power(2, 10) -> 1024
#   power(5, 0)  -> 1
# База: exp == 0 -> 1. Шаг: base * power(base, exp - 1).
#
# def power(base: int, exp: int) -> int:
#     ...


# === 5. gcd ===
# НОД по алгоритму Евклида, рекурсивно.
#   gcd(48, 18) -> 6
#   gcd(7, 0)   -> 7
# Подсказка: gcd(a, b) = gcd(b, a % b), база — b == 0.
#
# def gcd(a: int, b: int) -> int:
#     ...


# === 6. flatten ===
# Развернуть произвольно вложенный список в плоский.
#   flatten([1, [2, [3, 4], 5], [6]]) -> [1, 2, 3, 4, 5, 6]
#   flatten([])                       -> []
# Подсказка: isinstance(item, list) — углубляемся, иначе добавляем элемент.
#
# def flatten(data: list) -> list:
#     ...


# === 7. is_palindrome ===
# Палиндром ли строка (рекурсивно).
#   is_palindrome("level")  -> True
#   is_palindrome("python") -> False
#   is_palindrome("a")      -> True
# Подсказка: сравни края s[0] и s[-1], рекурсивно проверь середину s[1:-1].
# База: длина 0 или 1 -> True.
#
# def is_palindrome(s: str) -> bool:
#     ...


def demo6():
    print("Задачи на рекурсию: раскомментируй задание и проверки ниже.")

    # print(sum_to(5))                          # 15
    # print(count_digits(12345))                # 5
    # print(reverse_string("abc"))              # cba
    # print(power(2, 10))                       # 1024
    # print(gcd(48, 18))                        # 6
    # print(flatten([1, [2, [3, 4], 5], [6]]))  # [1, 2, 3, 4, 5, 6]
    # print(is_palindrome("level"))             # True
    # print(is_palindrome("python"))            # False


if __name__ == "__main__":
    demo6()
