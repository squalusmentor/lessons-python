# Урок L5.6 — Композиция против наследования
#
# Наследование: "X ЯВЛЯЕТСЯ Y" (IS-A).  Композиция: "X СОДЕРЖИТ Y" (HAS-A).
# Правило: предпочитай композицию. Наследуйся, только если подкласс
# действительно ЯВЛЯЕТСЯ родителем и обязан быть с ним взаимозаменяем.


# --- АНТИПРИМЕР: Stack наследует list ---
# Беда: Stack получает ВСЁ протекающее API списка (append, insert, sort, [i]=...),
# хотя стек обязан давать только push/pop. Инкапсуляция сломана наследованием.
class StackBad(list):
    def push(self, x):
        self.append(x)
    # pop() уже есть у list — но есть и insert/sort/reverse, которые тут лишние.


# --- ПРАВИЛЬНО: Stack СОДЕРЖИТ list (композиция + делегирование) ---
class Stack:
    def __init__(self):
        self._items = []              # список ВНУТРИ, наружу не торчит

    def push(self, x):
        self._items.append(x)         # делегируем работу внутреннему списку

    def pop(self):
        return self._items.pop()

    def __len__(self):
        return len(self._items)


# --- Композиция как сборка из частей ---
class Engine:
    def __init__(self, power):
        self.power = power

    def start(self):
        return f"двигатель {self.power} л.с. заведён"


class Car:
    def __init__(self, model, power):
        self.model = model
        self.engine = Engine(power)   # Car СОДЕРЖИТ Engine (а не наследует его)

    def start(self):
        return f"{self.model}: " + self.engine.start()   # делегирование


def demo6():
    print("-- антипример: наследование от list протекает --")
    bad = StackBad()
    bad.push(1)
    bad.push(2)
    bad.insert(0, 999)   # так делать нельзя, но list это разрешил
    print("  StackBad после insert(0, 999):", list(bad), "-> смысл стека сломан")

    print("-- композиция: наружу только push/pop --")
    s = Stack()
    s.push("a")
    s.push("b")
    print("  len(s) =", len(s))
    print("  s.pop() =", s.pop())
    print("  у Stack нет insert/sort — и это правильно")

    print("-- композиция как сборка из частей --")
    car = Car("Lada", 90)
    print("  ", car.start())


if __name__ == "__main__":
    demo6()
