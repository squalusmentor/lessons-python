"""
Урок B1 — РЕШЕНИЯ задач на рекурсию (06_recursion_tasks.py).

Запуск:  python solutions/recursion_tasks_solution.py
"""


# 1. Сумма 1..n
def sum_to(n: int) -> int:
    if n == 1:               # база
        return 1
    return n + sum_to(n - 1)  # шаг


# 2. Число цифр (без str)
def count_digits(n: int) -> int:
    if n < 10:               # база: одна цифра (включая 0)
        return 1
    return 1 + count_digits(n // 10)


# 3. Переворот строки
def reverse_string(s: str) -> str:
    if s == "":              # база
        return ""
    return reverse_string(s[1:]) + s[0]


# 4. Возведение в степень
def power(base: int, exp: int) -> int:
    if exp == 0:             # база
        return 1
    return base * power(base, exp - 1)


# 5. НОД (Евклид)
def gcd(a: int, b: int) -> int:
    if b == 0:               # база
        return a
    return gcd(b, a % b)


# 6. Расплющить вложенный список
def flatten(data: list) -> list:
    result = []
    for item in data:
        if isinstance(item, list):
            result += flatten(item)   # шаг: углубляемся
        else:
            result.append(item)
    return result


# 7. Палиндром
def is_palindrome(s: str) -> bool:
    if len(s) <= 1:          # база
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])


def demo():
    print("sum_to(5)        =", sum_to(5))                          # 15
    print("count_digits(12345) =", count_digits(12345))            # 5
    print("count_digits(0)  =", count_digits(0))                    # 1
    print("reverse_string   =", reverse_string("abc"))             # cba
    print("power(2, 10)     =", power(2, 10))                       # 1024
    print("gcd(48, 18)      =", gcd(48, 18))                        # 6
    print("flatten          =", flatten([1, [2, [3, 4], 5], [6]]))  # 1..6
    print("is_palindrome    =", is_palindrome("level"), is_palindrome("python"))  # True False


if __name__ == "__main__":
    demo()
