# Урок B6.2 -- Event loop: как один поток крутит много корутин
#
# Конкурентность без параллелизма. Один поток, один event loop. Пока одна
# корутина ждёт в точке await, loop выполняет другие. Переключение происходит
# ТОЛЬКО в точках await -- это кооперативная многозадачность (в отличие от
# потоков, которые ОС вытесняет когда захочет, в любой точке кода).
import asyncio
import time

START = 0.0


def stamp() -> str:
    return f"[{time.perf_counter() - START:.2f}с]"


async def worker(name: str, steps: int, pause: float):
    for i in range(1, steps + 1):
        await asyncio.sleep(pause)          # точка переключения: отдаём управление loop'у
        print(f"  {stamp()} {name}: шаг {i}/{steps}")


async def main_sequential():
    global START
    START = time.perf_counter()
    # Каждый воркер await'ится до конца перед следующим -- наложения нет.
    await worker("A", 3, 0.3)
    await worker("B", 3, 0.3)
    print(f"  последовательно: {time.perf_counter() - START:.2f} с (~1.8 с)")


async def main_gather():
    global START
    START = time.perf_counter()
    # gather стартует корутины ВМЕСТЕ и ждёт их все. Их паузы накладываются:
    # пока один спит, работают другие -- поэтому ~0.9 с, а не 1.8 с.
    await asyncio.gather(
        worker("A", 3, 0.3),
        worker("B", 3, 0.3),
    )
    print(f"  через gather: {time.perf_counter() - START:.2f} с (~0.9 с)")


async def main_tasks():
    global START
    START = time.perf_counter()
    # create_task планирует корутину в loop и СРАЗУ возвращает Task-объект;
    # работа уже пошла в фоне. Забрать результат -- позже, через await task.
    task = asyncio.create_task(worker("фон", 3, 0.3))
    print(f"  {stamp()} задача создана, основной код продолжает работать")
    await asyncio.sleep(0.5)
    print(f"  {stamp()} основной код успел сделать что-то своё...")
    await task                              # дожидаемся фоновую задачу
    print(f"  {stamp()} фоновая задача завершена")


def demo2():
    print("-- два await подряд: наложения НЕТ (сумма времён) --")
    asyncio.run(main_sequential())
    print("-- gather: корутины конкурентны (паузы накладываются) --")
    asyncio.run(main_gather())
    print("-- create_task: запускаем в фон, забираем результат позже --")
    asyncio.run(main_tasks())


if __name__ == "__main__":
    demo2()
