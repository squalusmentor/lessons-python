# Урок B1.3 — Замыкания: вложенные функции, захват переменных, nonlocal


# Вложенная функция ВИДИТ переменные объемлющей. Это замыкание.
# Захваченная переменная живёт вместе с возвращённой функцией.
def multiplier(factor: int):
    def inner(x: int) -> int:
        return x * factor    # factor захвачен из multiplier
    return inner             # возвращаем функцию; factor живёт вместе с ней


# nonlocal позволяет ИЗМЕНЯТЬ захваченную переменную (а не создавать локальную).
# Так получается "состояние без класса".
def make_counter():
    count = 0
    def increment() -> int:
        nonlocal count       # без этого count += 1 упадёт UnboundLocalError
        count += 1
        return count
    return increment


# Ловушка позднего связывания: все лямбды захватывают ОДНУ переменную i,
# а не её значение в момент создания.
def late_binding_trap():
    funcs = [lambda: i for i in range(3)]
    return [f() for f in funcs]   # [2, 2, 2], а не [0, 1, 2]


# Починка: захватить значение через аргумент по умолчанию (он вычисляется сразу).
def late_binding_fixed():
    funcs = [lambda i=i: i for i in range(3)]
    return [f() for f in funcs]   # [0, 1, 2]


def demo3():
    print("-- фабрика функций --")
    double = multiplier(2)
    triple = multiplier(3)
    print("  double(5) =", double(5))
    print("  triple(5) =", triple(5))

    print("-- счётчик с состоянием (nonlocal) --")
    c = make_counter()
    print("  c() =", c())  # 1
    print("  c() =", c())  # 2
    print("  c() =", c())  # 3
    c2 = make_counter()    # у каждого счётчика своё независимое состояние
    print("  новый счётчик c2() =", c2())  # 1

    print("-- ловушка позднего связывания --")
    print("  trap :", late_binding_trap())   # [2, 2, 2]
    print("  fixed:", late_binding_fixed())  # [0, 1, 2]

    print("-- заглянуть в захваченные переменные --")
    # __closure__ — кортеж ячеек с захваченными значениями.
    print("  double.__closure__:", [cell.cell_contents for cell in double.__closure__])


if __name__ == "__main__":
    demo3()
