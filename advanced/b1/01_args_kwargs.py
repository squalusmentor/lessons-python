# Урок B1.1 — *args и **kwargs: сбор и распаковка аргументов


# *args собирает ОСТАВШИЕСЯ позиционные аргументы в КОРТЕЖ.
def total(*nums: int) -> int:
    print(f"  внутри: nums = {nums} (тип {type(nums).__name__})")
    return sum(nums)


# **kwargs собирает ОСТАВШИЕСЯ именованные аргументы в СЛОВАРЬ.
def describe(**fields) -> None:
    print(f"  внутри: fields = {fields} (тип {type(fields).__name__})")
    for key, value in fields.items():
        print(f"    {key} = {value}")


# Полная сигнатура. Порядок строгий:
#   обычные позиционные -> *args -> только-именованные -> **kwargs
def make_request(method: str, *parts: str, timeout: int = 30, **headers) -> None:
    url = "/".join(parts)
    print(f"  {method} {url} (timeout={timeout})")
    for name, value in headers.items():
        print(f"    header {name}: {value}")


# Слэш `/` — параметры слева ТОЛЬКО-ПОЗИЦИОННЫЕ.
# Звёздочка `*` — параметры справа ТОЛЬКО-ИМЕНОВАННЫЕ.
def connect(host: str, port: int, /, *, secure: bool = True) -> None:
    proto = "https" if secure else "http"
    print(f"  {proto}://{host}:{port}")


# Проброс *args/**kwargs дальше — основа обёрток и декораторов:
# обёртка принимает что угодно и передаёт без изменений.
def logged(func, *args, **kwargs):
    print(f"  вызываю {func.__name__} с args={args} kwargs={kwargs}")
    return func(*args, **kwargs)


def demo1():
    # === *args: сбор позиционных в кортеж ===
    print("total(1, 2, 3) =", total(1, 2, 3))
    print("total(10, 20, 30, 40) =", total(10, 20, 30, 40))
    print("total() =", total())  # пустой кортеж — это нормально

    # === Распаковка списка в *args через * ===
    nums = [1, 2, 3, 4, 5]
    print("total(*nums) =", total(*nums))  # * разворачивает список в аргументы

    # === **kwargs: сбор именованных в словарь ===
    print("describe(name=..., age=...):")
    describe(name="Аня", age=25, city="Москва")

    # === Распаковка словаря в **kwargs через ** ===
    person = {"name": "Боря", "age": 30}
    describe(**person)  # ** разворачивает словарь в name=..., age=...

    # === Всё вместе: позиционные + *args + только-именованные + **kwargs ===
    make_request("GET", "api", "v1", "weather",
                 timeout=10,
                 Authorization="Bearer xyz", Accept="application/json")

    # === Только-позиционные / только-именованные ===
    connect("localhost", 5432)                 # ок
    connect("localhost", 5432, secure=False)   # secure — только по имени
    # connect(host="localhost", port=5432)     # TypeError: host/port только по позиции

    # === Проброс аргументов (паттерн обёртки) ===
    print("logged(total, ...) =", logged(total, 1, 2, 3))
    logged(describe, name="Вика", role="admin")


if __name__ == "__main__":
    demo1()
