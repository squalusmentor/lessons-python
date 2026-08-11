# Урок L6.3 — Декораторы с параметрами и functools.wraps
#
# Три уровня: фабрика (принимает ПАРАМЕТРЫ) -> декоратор (принимает ФУНКЦИЮ)
# -> обёртка (принимает АРГУМЕНТЫ вызова).
# @file_decorator("...") — это два вызова: f = file_decorator("...")(f)
import functools


def file_decorator(errormessage):
    def internal_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                print(errormessage)
                print(e)
                return False
        return wrapper
    return internal_decorator


@file_decorator("не удалось прочитать файл")
def read_config(path):
    """Читает текстовый файл целиком."""
    with open(path, encoding="utf-8") as f:
        return f.read()


@file_decorator("не удалось разобрать число")
def parse_number(text):
    """Превращает строку в int."""
    return int(text)


# Без functools.wraps декорированная функция теряет имя и докстринг.
def naive_decorator(function):
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper


def good_decorator(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper


@naive_decorator
def naive_func():
    """Докстринг naive_func."""


@good_decorator
def good_func():
    """Докстринг good_func."""


def demo3():
    print("-- file_decorator: исключение поймано, программа живёт --")
    print("  parse_number('42')  =", parse_number("42"))
    print("  parse_number('abc') =", parse_number("abc"))
    print("  read_config('no_such_file.cfg') =", read_config("no_such_file.cfg"))

    print("-- расшифровка @file_decorator('...') --")
    decorator = file_decorator("сообщение")   # 1-й вызов: фабрика вернула декоратор
    safe_int = decorator(int)                 # 2-й вызов: декоратор вернул обёртку
    print("  safe_int('5')  =", safe_int("5"))
    print("  safe_int('xx') =", safe_int("xx"))

    print("-- зачем functools.wraps --")
    print("  без wraps: __name__ =", naive_func.__name__, "| __doc__ =", naive_func.__doc__)
    print("  с wraps  : __name__ =", good_func.__name__, "| __doc__ =", good_func.__doc__)
    print("  parse_number.__name__ =", parse_number.__name__)


if __name__ == "__main__":
    demo3()
