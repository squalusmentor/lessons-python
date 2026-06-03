"""
Урок B2 — ПРАКТИЧЕСКАЯ РАБОТА, ЧАСТЬ 1 (Занятие 1: инкапсуляция, наследование,
полиморфизм, dunder).

Проект: CLI-менеджер инвентаря (склад/библиотека). В части 1 строим КЛАССЫ
ПРЕДМЕТОВ — фундамент. Сам менеджер (добавление/поиск/выдача) будет в части 2.

ООП здесь ради задачи: предмет обязан хранить свой инвариант (склад не уходит
в минус), а каталог должен печататься полиморфно, не зная конкретных типов.

Запуск:  python practice_inventory_part1.py
Решение: solutions/practice_inventory_part1_solution.py
"""


# === TODO 1. Базовый класс Item ===
# Поля (через __init__):
#   item_id  — str, инвентарный номер/артикул (уникальный идентификатор)
#   name     — str, название
#   quantity — int, количество на складе (храни в self._quantity)
#
# Инкапсуляция: количество меняем ТОЛЬКО методами restock/take, держащими
# инвариант "склад не уходит в минус". Снаружи количество читаем, но не пишем.
#
# Методы:
#   restock(n)  — добавить n штук (n > 0, иначе ValueError)
#   take(n)     — забрать n штук (1 <= n <= остаток, иначе ValueError)
#   label()     — строка для каталога. Базовая версия:
#                 f"[{item_id}] {name} — {quantity} шт."
#                 Это ПОЛИМОРФНАЯ точка: подклассы её дополнят.
#
# Dunder-методы:
#   __repr__    — для отладки, напр. Tool('A-1', 'Молоток', 5)
#                 (подсказка: type(self).__name__ даст имя реального класса)
#   __eq__      — равны, если совпадает item_id
#   __hash__    — согласован с __eq__ (hash по item_id) -> можно класть в set
#   __lt__      — сравнение по name (для sorted())
#
# class Item:
#     def __init__(self, item_id: str, name: str, quantity: int):
#         ...


# === TODO 2. Подкласс Book(Item) ===
# Добавляет поле author (str). Зови super().__init__(...).
# Переопредели label(): к базовой строке добавь ", автор: <author>".
#
# class Book(Item):
#     ...


# === TODO 3. Подкласс Tool(Item) ===
# Добавляет поле condition (str, по умолчанию "новый").
# Переопредели label(): к базовой строке добавь ", состояние: <condition>".
#
# class Tool(Item):
#     ...


# === TODO 4. print_catalog(items) — полиморфизм в действии ===
# Принимает список РАЗНЫХ предметов и печатает label() каждого.
# Цикл не знает конкретный тип — просто зовёт it.label().
#
# def print_catalog(items) -> None:
#     ...


def demo():
    print("== Часть 1: классы предметов ==")
    # Раскомментируй блоки по мере выполнения TODO.

    # hammer = Tool("A-1", "Молоток", 5)
    # book = Book("B-1", "Чистый код", 3, author="Роберт Мартин")
    # clip = Item("C-1", "Скрепка", 1000)

    # print("-- label() полиморфен --")
    # print_catalog([hammer, book, clip])

    # print("-- инкапсуляция: инвариант склада --")
    # hammer.take(2)
    # print("  после take(2):", hammer.label())
    # try:
    #     hammer.take(100)
    # except ValueError as e:
    #     print("  поймали:", e)

    # print("-- dunder: ==, hash, сортировка --")
    # print("  равенство по item_id:", book == Book("B-1", "x", 0, "y"))
    # print("  set без дублей по id:", {hammer, book, clip})
    # print("  sorted по имени:", [it.name for it in sorted([hammer, book, clip])])


if __name__ == "__main__":
    demo()
