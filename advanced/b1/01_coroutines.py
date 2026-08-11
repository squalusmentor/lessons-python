# Урок B1.1 -- Корутины: async def, await, asyncio.run
#
# Первое, что нужно усвоить: ВЫЗОВ async-функции ничего не выполняет. Он лишь
# создаёт объект-корутину -- "рецепт" работы, который кто-то должен запустить.
# Запускает event loop, а входная дверь в него -- asyncio.run().
import asyncio
import time


async def greet(name: str, delay: float) -> str:
    # await asyncio.sleep -- это НЕ time.sleep. Он не блокирует поток, а говорит
    # event loop'у: "усыпи меня на delay секунд и займись другими корутинами".
    await asyncio.sleep(delay)
    return f"привет, {name}"


async def main_sequential():
    # Два await подряд -- это ПОСЛЕДОВАТЕЛЬНО: вторая корутина стартует только
    # после того, как завершилась первая. Суммарное время ~= сумме задержек.
    start = time.perf_counter()
    first = await greet("Аня", 1.0)
    second = await greet("Боря", 1.0)
    elapsed = time.perf_counter() - start
    print(f"  получили: {first!r}, затем {second!r}")
    print(f"  два последовательных await заняли {elapsed:.2f} с (~2 с)")


def demo1():
    print("-- вызов async-функции возвращает корутину, а не результат --")
    coro = greet("мир", 0)                      # тело greet ещё НЕ выполнялось
    print("  тип объекта:", type(coro).__name__)   # coroutine
    # Корутину нужно либо await'ить внутри другой корутины, либо отдать в
    # asyncio.run -- он поднимет event loop, прокрутит корутину и вернёт итог.
    result = asyncio.run(coro)                  # вот теперь тело greet отработало
    print("  результат после asyncio.run:", repr(result))

    print("-- await по очереди: последовательное выполнение --")
    asyncio.run(main_sequential())

    print("-- забыл await? Python предупредит 'coroutine was never awaited' --")
    forgotten = greet("призрак", 0)             # создали, но не запустили
    print("  создан висячий объект:", type(forgotten).__name__)
    forgotten.close()                           # закрываем вручную, чтобы не ругался


if __name__ == "__main__":
    demo1()
