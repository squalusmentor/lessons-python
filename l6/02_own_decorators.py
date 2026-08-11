# Урок L6.2 — Собственные декораторы: для функций и методов класса
#
# Декоратор принимает функцию и возвращает её замену (обёртку).
# Строка @log_calls — синтаксический сахар для add = log_calls(add).


def log_calls(function):
    def wrapper(*args, **kwargs):
        print(f"  [log] вызов {function.__name__}, args={args}, kwargs={kwargs}")
        result = function(*args, **kwargs)
        print(f"  [log] {function.__name__} вернула {result!r}")
        return result            # без return все функции вернут None
    return wrapper


@log_calls
def add(a, b):
    return a + b


# То же самое без @ — видно, что никакой новой механики нет.
def sub(a, b):
    return a - b

sub = log_calls(sub)


# Метод — та же функция, self проедет через *args. Декоратор тот же.
class Cart:
    def __init__(self):
        self.items = []

    @log_calls
    def add_item(self, name: str, price: int):
        self.items.append((name, price))
        return len(self.items)

    @log_calls
    def total(self):
        return sum(price for _, price in self.items)


# Порядок применения: снизу вверх, f = exclaim(parenthesize(f)).
def exclaim(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs) + "!"
    return wrapper


def parenthesize(function):
    def wrapper(*args, **kwargs):
        return "(" + function(*args, **kwargs) + ")"
    return wrapper


@exclaim
@parenthesize
def greet(name):
    return f"привет, {name}"


def demo2():
    print("-- декоратор через @ --")
    print("  add(2, 3) =", add(2, 3))

    print("-- то же руками: sub = log_calls(sub) --")
    print("  sub(7, 4) =", sub(7, 4))

    print("-- имя снаружи теперь wrapper (починим в L6.3) --")
    print("  add.__name__ =", add.__name__)

    print("-- декоратор на методах класса --")
    cart = Cart()
    cart.add_item("хлеб", 40)
    cart.add_item("молоко", 80)
    print("  итого:", cart.total())

    print("-- несколько декораторов: снизу вверх --")
    print("  greet('Аня') =", greet("Аня"))


if __name__ == "__main__":
    demo2()
