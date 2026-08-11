# Урок L3.3 — Списки: методы и срезы


def demo3():

    # === Базовые методы изменения ===
    print("-- append / extend / insert --")
    nums = [3, 1, 2]
    nums.append(4)          # добавить один в конец
    print("после append:", nums)
    nums.extend([5, 6])     # добавить несколько
    print("после extend:", nums)
    nums.insert(0, 9)       # вставить по индексу
    print("после insert:", nums)

    # === Удаление: remove (по значению), pop (по индексу, возвращает) ===
    print("-- remove / pop --")
    nums.remove(9)          # удалить первое вхождение значения 9
    print("после remove(9):", nums)
    last = nums.pop()       # снять последний и вернуть
    print("pop() вернул:", last, "| список:", nums)

    # === Поиск и подсчёт ===
    print("-- count / index --")
    letters = ["a", "b", "a", "c", "a"]
    print("count('a') =", letters.count("a"))
    print("index('c') =", letters.index("c"))

    # === sort() меняет список; sorted() возвращает новый ===
    print("-- sort vs sorted --")
    data = [3, 1, 2]
    data.sort()
    print("data после sort():", data)
    src = [3, 1, 2]
    ordered = sorted(src)
    print("sorted(src) =", ordered, "| src не изменился:", src)
    print("sorted(reverse=True) =", sorted(src, reverse=True))

    # === Срезы (slices) ===
    print("-- срезы --")
    seq = [10, 20, 30, 40, 50]
    print("seq[1:4]  =", seq[1:4])    # [20, 30, 40]
    print("seq[:2]   =", seq[:2])     # [10, 20]
    print("seq[::-1] =", seq[::-1])   # разворот
    copy = seq[:]                     # полная копия
    copy.append(60)
    print("копия не трогает оригинал:", seq, copy)


if __name__ == "__main__":
    demo3()
