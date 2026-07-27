# Урок B8.1 — Итераторы: что происходит внутри for
#
# Три слова, которые надо развести раз и навсегда:
#   iterable (итерируемое) — то, ПО ЧЕМУ можно пройти: список, строка, словарь, файл;
#   iterator (итератор)    — тот, КТО идёт: помнит позицию и умеет next();
#   for                    — цикл, который сам берёт итератор и сам дергает next().
#
# Зачем это знать: перестанешь удивляться, почему "второй цикл по тому же
# объекту ничего не вывел" и почему zip, enumerate и файл ведут себя именно так.

from pathlib import Path

DATA_PATH = Path(__file__).parent / "demo_lines.txt"


def manual_loop():
    """for изнутри: iter() -> next() -> StopIteration."""
    numbers = [10, 20, 30]

    it = iter(numbers)                  # 1) for первым делом просит итератор
    print("  next(it) =", next(it))     # 2) и дальше просто дергает next()
    print("  next(it) =", next(it))
    print("  next(it) =", next(it))
    try:
        next(it)                        # 3) значения кончились -> StopIteration
    except StopIteration:
        print("  next(it) -> StopIteration, значения кончились")


def for_by_hand(iterable):
    """Ровно то, что делает обычный for. В жизни так писать не надо."""
    it = iter(iterable)
    while True:
        try:
            value = next(it)
        except StopIteration:
            break                       # for ловит StopIteration и тихо выходит
        print("  значение:", value)


def one_shot():
    """Итератор одноразовый: пройти по нему второй раз нельзя."""
    numbers = [1, 2, 3]

    it = iter(numbers)
    print("  первый проход по итератору:", list(it))
    print("  второй проход по итератору:", list(it), "<- пусто, он уже израсходован")
    print("  а по самому списку:", list(numbers), "и ещё раз:", list(numbers))


def read_line_by_line():
    """Так читают файлы: открытый файл — итератор, он выдаёт строки по одной."""
    with open(DATA_PATH, encoding="utf-8") as f:
        for line in f:                  # в памяти одна строка, а не весь файл
            print("  ", line.strip())


def read_whole_file():
    """А так файл читают в память целиком."""
    with open(DATA_PATH, encoding="utf-8") as f:
        lines = f.readlines()           # весь файл сразу списком строк
        print("  ", lines)


class Countdown:
    """Свой итератор: обратный отсчёт от start до 1.

    Чтобы объект работал в for, ему нужны всего два метода:
      __iter__ — вернуть итератор (здесь сам объект, поэтому return self);
      __next__ — выдать следующее значение или бросить StopIteration.
    """

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current < 1:
            raise StopIteration     # конец: без этого цикл будет бесконечным
        value = self.current
        self.current -= 1
        return value


def demo1():
    print("== 01. Итераторы: что внутри for ==\n")

    print("-- iter() и next() руками --")
    manual_loop()

    print("\n-- то же самое, но циклом while (это и есть for) --")
    for_by_hand("абв")              # строка тоже iterable

    print("\n-- итератор одноразовый, а список - нет --")
    one_shot()

    print("\n-- где это нужно на практике: файл - это итератор строк --")
    print("  идём по файлу построчно (for line in f):")
    read_line_by_line()
    print("  а тут readlines() загрузил файл в память целиком:")
    read_whole_file()
    # На трёх строках разницы нет. На файле в 2 ГБ первый вариант работает,
    # второй кладёт программу: readlines() тянет в память сразу всё.

    print("\n-- свой итератор: класс с __iter__ и __next__ --")
    for number in Countdown(5):
        print("  осталось:", number)

    print("\nИтог: iterable отдаёт итератор, итератор выдаёт значения по одному")
    print("и заканчивается StopIteration. Класс из 12 строк - это многовато;")
    print("в файле 02 то же самое уместится в две строки через yield.")


if __name__ == "__main__":
    demo1()
