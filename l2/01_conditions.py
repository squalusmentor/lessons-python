# Урок 2.1 — Условия: if / elif / else, тернарный оператор, match


def demo1():

    # === if / else ===
    age = 18
    if age >= 18:
        print("совершеннолетний")
    else:
        print("несовершеннолетний")

    # === if / elif / else ===
    score = 75
    if score >= 90:
        print("отлично")
    elif score >= 70:
        print("хорошо")
    elif score >= 50:
        print("удовлетворительно")
    else:
        print("неудовлетворительно")

    # === Истинность (truthy / falsy) ===
    # Любое значение в if приводится к bool.
    # Ложные: False, None, 0, 0.0, "", [], {}, (), set()
    nums = []
    if nums:
        print("список не пуст")
    else:
        print("список пустой")  # сработает эта ветка

    name = "Аня"
    if name:
        print(f"имя задано: {name}")

    # === Тернарный оператор (условное выражение) ===
    n = 42
    parity = "чётное" if n % 2 == 0 else "нечётное"
    print(n, parity)

    # === match / case (Python 3.10+) ===
    day = 4
    match day:
        case 1:
            print("понедельник")
        case 2:
            print("вторник")
        case 3:
            print("среда")
        case 6 | 7:
            # несколько значений — через |
            print("выходной")
        case _:
            # _ — wildcard, аналог default
            print("другой день")

    # === Замена длинной цепочки elif: пишут именно elif, а не match ===
    temp = 15
    if temp < 0:
        print("холодно")
    elif temp < 20:
        print("прохладно")
    elif temp < 30:
        print("тепло")
    else:
        print("жарко")


if __name__ == "__main__":
    demo1()
