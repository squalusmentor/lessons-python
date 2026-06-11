# Урок B3.1 — Напоминание: вложенные функции и замыкания (база для декораторов)
#
# Два факта из B1, без которых декоратор не понять:
#   1) функция — объект: её можно передать и вернуть;
#   2) вложенная функция захватывает переменные внешней (замыкание).


def shout(text: str) -> str:
    return text.upper() + "!"


def whisper(text: str) -> str:
    return text.lower() + "..."


# Функция как аргумент: apply ничего не знает о shout/whisper.
def apply(func, value):
    return func(value)


# Функция как результат: multiplier — фабрика функций.
def multiplier(factor: int):
    def inner(x: int) -> int:
        return x * factor    # factor захвачен из multiplier
    return inner


# nonlocal — чтобы ИЗМЕНЯТЬ захваченную переменную, а не создавать локальную.
def make_counter():
    count = 0
    def increment() -> int:
        nonlocal count
        count += 1
        return count
    return increment


# Шаг до декоратора: принимаем функцию, возвращаем новую функцию вокруг неё.
def make_loud(func):
    def louder(text):
        return func(text).upper()
    return louder


def demo1():
    print("-- функция как аргумент --")
    print("  apply(shout, 'привет')   =", apply(shout, "привет"))
    print("  apply(whisper, 'ПРИВЕТ') =", apply(whisper, "ПРИВЕТ"))

    print("-- функция как результат (замыкание) --")
    double = multiplier(2)
    triple = multiplier(3)
    print("  double(5) =", double(5))
    print("  triple(5) =", triple(5))

    print("-- nonlocal: состояние внутри замыкания --")
    c = make_counter()
    print("  c() =", c())
    print("  c() =", c())
    print("  c() =", c())

    print("-- полшага до декоратора: функция из функции --")
    loud_whisper = make_loud(whisper)
    print("  loud_whisper('Тссс') =", loud_whisper("Тссс"))
    print("  имя снаружи:", loud_whisper.__name__)


if __name__ == "__main__":
    demo1()
