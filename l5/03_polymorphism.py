# Урок L5.3 — Полиморфизм и утиная типизация
#
# Полиморфизм: один и тот же вызов (obj.label()) ведёт себя по-разному в
# зависимости от типа объекта. Код, перебирающий объекты, НЕ должен знать их
# конкретный класс — ему важен только общий ИНТЕРФЕЙС (набор методов).
from abc import ABC, abstractmethod


# --- Утиная типизация: общего предка нет, а интерфейс есть ---
# "Если выглядит как утка и крякает как утка — считаем уткой."
class Cat:
    def voice(self) -> str:
        return "Мяу"


class Dog:
    def voice(self) -> str:
        return "Гав"


class Duck:
    def voice(self) -> str:
        return "Кря"


def chorus(animals) -> None:
    # Нам всё равно, какой это класс. Лишь бы умел voice().
    for a in animals:
        print("  ", a.voice())


# --- Абстрактный базовый класс (abc): задаёт КОНТРАКТ ---
# Создать сам Shape нельзя — можно только наследников, реализовавших area().
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h


class Circle(Shape):
    def __init__(self, r):
        self.r = r

    def area(self) -> float:
        return 3.14159 * self.r ** 2


def demo3():
    print("-- утиная типизация: разные классы, общий интерфейс --")
    chorus([Cat(), Dog(), Duck()])

    print("-- полиморфизм: один цикл, разные area() --")
    shapes = [Rect(3, 4), Circle(5), Rect(2, 2)]
    for s in shapes:
        print(f"   {type(s).__name__}: area = {s.area():.2f}")
    total = sum(s.area() for s in shapes)   # зовём area() не зная конкретный тип
    print("  суммарная площадь =", round(total, 2))

    print("-- abc не даёт создать абстрактный класс --")
    try:
        Shape()
    except TypeError as e:
        print("  поймали TypeError:", e)


if __name__ == "__main__":
    demo3()
