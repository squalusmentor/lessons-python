# Урок 2.2 — Циклы: for, while, range, break, continue, for-else, enumerate, zip


def demo2():

    # === for по range — аналог классического for-счётчика ===
    print("-- for + range --")
    for i in range(5):
        print("i =", i)

    # === range с шагом и от-до ===
    print("-- range(1, 10, 2) --")
    for i in range(1, 10, 2):
        print(i)

    # === while ===
    print("-- while --")
    n = 10
    while n > 0:
        print("n =", n)
        n -= 3

    # === Бесконечный цикл + break ===
    print("-- while True + break --")
    count = 0
    while True:
        if count == 3:
            break
        print("count =", count)
        count += 1

    # === continue: пропустить итерацию ===
    print("-- continue --")
    for i in range(10):
        if i % 2 == 0:
            continue  # пропустить чётные
        print("нечётное:", i)

    # === for по списку — естественная итерация ===
    print("-- for по списку --")
    nums = [10, 20, 30, 40]
    for val in nums:
        print(val)

    # === Когда нужен индекс — enumerate, а не range(len(...)) ===
    print("-- enumerate --")
    for idx, val in enumerate(nums):
        print(f"index={idx} value={val}")

    # === Параллельная итерация ===
    print("-- zip --")
    names = ["Аня", "Боря", "Вика"]
    ages = [25, 30, 22]
    # zip создает кортежи из элементов списка list(zip('abcdefg', range(3), range(4))) 
    # [('a', 0, 0), ('b', 1, 1), ('c', 2, 2)]
    for name, age in zip(names, ages):
        print(f"{name}: {age}")

    # === for по строке — посимвольно ===
    print("-- for по строке --")
    for ch in "Python!":
        print(f"символ={ch} код={ord(ch)}")

    # === for / else — выполнится, если цикл прошёл БЕЗ break ===
    print("-- for / else --")
    target = 99
    for x in nums:
        if x == target:
            print("нашли")
            break
    else:
        print(f"{target} не найден")

    # === Вложенные циклы — таблица умножения ===
    print("-- вложенные циклы --")
    for i in range(1, 4):
        for j in range(1, 4):
            print(f"{i}*{j}={i*j}", end="  ")
        print()


if __name__ == "__main__":
    demo2()
