# Урок 2.4 — ПРАКТИКА
#
# Как пользоваться:
#   1. Раскомментируй нужное задание (функцию и описание).
#   2. Допиши реализацию вместо заглушки.
#   3. В demo4() раскомментируй вызов и запусти файл (python 04_practice.py).


# === Задание 1. is_leap_year ===
# Год високосный, если он делится на 4, НО не делится на 100,
# кроме случаев, когда делится на 400.
#   2000 -> True  (делится на 400)
#   1900 -> False (делится на 100, но не на 400)
#   2024 -> True
#   2023 -> False
#
# def is_leap_year(year: int) -> bool:
#     return False


# === Задание 2. fizz_buzz ===
# Напечатай числа от 1 до n включительно, по одному на строку.
# Вместо кратных 3  — "Fizz".
# Вместо кратных 5  — "Buzz".
# Вместо кратных 15 — "FizzBuzz".
#   fizz_buzz(15) -> 1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz
#
# def fizz_buzz(n: int) -> None:
#     pass


# === Задание 3. max_in_list ===
# Верни максимальное число в списке. Для пустого списка верни 0.
# (Встроенный max() использовать НЕЛЬЗЯ — пройди циклом сам.)
#   max_in_list([3, 1, 4, 1, 5, 9, 2, 6]) -> 9
#   max_in_list([-5, -2, -9])             -> -2
#   max_in_list([])                       -> 0
#
# def max_in_list(nums: list[int]) -> int:
#     return 0


# === Задание 4. is_prime ===
# Простое число делится только на 1 и на само себя.
#   0, 1 и отрицательные — НЕ простые.
#   2 — простое.
#   4 — нет, 7 — да, 9 — нет, 17 — да.
# Подсказка: достаточно проверить делители до sqrt(n).
# Ещё подсказка: sqrt не обязателен — хватит условия i*i <= n.
#
# def is_prime(n: int) -> bool:
#     return False


# === Задание 5. reverse_list ===
# Верни НОВЫЙ список с элементами в обратном порядке.
# Исходный список менять не надо.
# (Срез [::-1] использовать НЕЛЬЗЯ — пройди циклом.)
#   reverse_list([1, 2, 3, 4]) -> [4, 3, 2, 1]
#   reverse_list([])           -> []
#
# def reverse_list(nums: list[int]) -> list[int]:
#     return []


# === Задание 6. digit_sum ===
# Сумма цифр числа. Отрицательные считай как положительные.
#   digit_sum(1234) -> 10
#   digit_sum(-99)  -> 18
#   digit_sum(0)    -> 0
#
# def digit_sum(n: int) -> int:
#     return 0


# === Задание 7. count_vowels ===
# Сосчитай гласные (a, e, i, o, u) в строке. Регистр игнорируй.
# Считаем только английские гласные.
#   count_vowels("Hello, World!") -> 3
#   count_vowels("Python")        -> 1
#   count_vowels("bcd")           -> 0
# Подсказка: в Python for по строке идёт посимвольно — никаких байтов.
#
# def count_vowels(s: str) -> int:
#     return 0


def demo4():
    print("Практика: раскомментируй задание и добавь вызов ниже.")

    # --- вызовы для проверки (раскомментируй, когда функция готова) ---

    # print(is_leap_year(2000))  # True
    # print(is_leap_year(1900))  # False
    # print(is_leap_year(2024))  # True

    # fizz_buzz(20)

    # print(max_in_list([3, 1, 4, 1, 5, 9, 2, 6]))  # 9
    # print(max_in_list([-5, -2, -9]))              # -2
    # print(max_in_list([]))                        # 0

    # print(is_prime(2))   # True
    # print(is_prime(4))   # False
    # print(is_prime(17))  # True

    # print(reverse_list([1, 2, 3, 4]))  # [4, 3, 2, 1]

    # print(digit_sum(1234))  # 10
    # print(digit_sum(-99))   # 18

    # print(count_vowels("Hello, World!"))  # 3
    # print(count_vowels("Python"))         # 1


if __name__ == "__main__":
    demo4()
