# Урок T1.5 — Кратко: кортежи, множества, словари


def demo5():

    # === Кортеж (tuple) — неизменяемый список ===
    print("-- кортеж --")
    point = (10, 20)
    x, y = point            # распаковка
    print("x =", x, "y =", y)
    # point[0] = 99         # -> TypeError: кортеж менять нельзя

    # === Множество (set) — уникальные элементы, быстрый поиск ===
    print("-- множество --")
    tags = {"bug", "ui", "bug", "api"}
    print("без дубликатов:", tags)
    print("'ui' in tags ->", "ui" in tags)
    print("убрать дубли из списка:", list(set([1, 1, 2, 3, 3, 3])))

    # === Словарь (dict) — пары ключ -> значение ===
    print("-- словарь --")
    case = {"name": "test_login", "status": "pass"}
    print("status =", case["status"])

    print("-- перебор словаря --")
    for key, value in case.items():
        print(key, "=", value)

    # === Счётчик на словаре через .get() ===
    print("-- счётчик на dict --")
    counts = {}
    for tag in ["bug", "ui", "bug", "bug", "ui"]:
        counts[tag] = counts.get(tag, 0) + 1
    print(counts)


if __name__ == "__main__":
    demo5()
