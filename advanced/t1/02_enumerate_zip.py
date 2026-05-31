# Урок T1.2 — enumerate и zip


def demo2():

    fruits = ["яблоко", "банан", "вишня"]

    # === Плохо: ручной счётчик ===
    print("-- ручной счётчик (так не надо) --")
    i = 0
    for fruit in fruits:
        print(i, fruit)
        i += 1

    # === Хорошо: enumerate ===
    print("-- enumerate --")
    for i, fruit in enumerate(fruits):
        print(i, fruit)

    # === enumerate со стартом не с нуля ===
    print("-- enumerate(start=1) --")
    for number, fruit in enumerate(fruits, start=1):
        print(f"{number}. {fruit}")

    # === zip: идём по двум спискам параллельно ===
    print("-- zip --")
    names = ["Аня", "Боря", "Вика"]
    scores = [90, 75, 88]
    for name, score in zip(names, scores):
        print(f"{name}: {score} баллов")

    # === zip останавливается по самому короткому списку ===
    print("-- zip разной длины --")
    for a, b in zip([1, 2, 3], ["x", "y"]):
        print(a, b)

    # === zip + dict: собрать словарь из двух списков ===
    print("-- dict(zip(...)) --")
    ages = dict(zip(names, [25, 30, 22]))
    print(ages)


if __name__ == "__main__":
    demo2()
