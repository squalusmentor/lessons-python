# Урок L6.4 — Рабочие декораторы: @timer, @retry, @cache
#
# Смысл декоратора — вынести обвязку (замер, повторы, кеш) из тела функции.
# Декоратор ничего не знает о функции, которую оборачивает, — поэтому один
# и тот же @retry годится и для запроса к API, и для чтения файла.
import functools
import time


def timer(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [timer] {function.__name__}: {elapsed:.4f} с")
        return result
    return wrapper


def retry(attempts: int = 3, delay: float = 0.5):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return function(*args, **kwargs)
                except Exception as e:
                    print(f"  [retry] попытка {attempt}/{attempts} упала: {e}")
                    if attempt == attempts:
                        raise               # попытки кончились — пробрасываем
                    time.sleep(delay)
        return wrapper
    return decorator


@timer
def slow_sum(n: int) -> int:
    return sum(range(n))


# Имитация нестабильного сетевого вызова: первые два раза падает, потом работает.
_calls = {"count": 0}


@retry(attempts=5, delay=0.1)
def flaky_fetch():
    _calls["count"] += 1
    if _calls["count"] < 3:
        raise ConnectionError("сервер не ответил")
    return {"status": "ok", "data": [1, 2, 3]}


def demo4():
    print("-- @timer: где тормозит --")
    slow_sum(5_000_000)

    print("-- @retry: переживаем временные сбои --")
    print("  flaky_fetch() =", flaky_fetch())

if __name__ == "__main__":
    demo4()
