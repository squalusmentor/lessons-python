# Урок T1.1 — Циклы: for, while, range, break, continue, for-else


def demo1():

    # === for по range — повторить действие N раз ===
    print("-- for + range(5) --")
    for i in range(5):
        print("i =", i)

    # === range: старт, стоп, шаг ===
    print("-- range(2, 11, 2) --")
    for i in range(2, 11, 2):
        print(i)

    # === range с отрицательным шагом — обратный отсчёт ===
    print("-- range(5, 0, -1) --")
    for i in range(5, 0, -1):
        print(i)

    # range НЕ список: чтобы увидеть числа списком — оборачиваем в list()
    print("list(range(1, 6)) =", list(range(1, 6)))

    # === while — пока условие истинно ===
    print("-- while --")
    balance = 100
    while balance > 0:
        balance -= 30
        print("осталось:", balance)

    # === Бесконечный цикл + break (аналог do-while) ===
    print("-- while True + break --")
    count = 0
    while True:
        if count == 3:
            break
        print("count =", count)
        count += 1

    # === continue: пропустить текущий шаг ===
    print("-- continue: только нечётные --")
    for i in range(1, 11):
        if i % 2 == 0:
            continue
        print(i)

    # === for / else: else сработает, если НЕ было break ===
    print("-- for / else (нашли) --")
    secret = 3
    for guess in range(1, 6):
        if guess == secret:
            print("угадал:", guess)
            break
    else:
        print("не нашли")

    print("-- for / else (не нашли) --")
    secret = 99
    for guess in range(1, 6):
        if guess == secret:
            print("угадал:", guess)
            break
    else:
        print("не нашли число в диапазоне")


if __name__ == "__main__":
    demo1()
