# Урок B6.6 -- Когда нативного async-клиента нет: run_in_executor и процессы
#
# Не для всего есть async-библиотека. Два спасательных приёма:
#   1) БЛОКИРУЮЩИЙ I/O-код без async-версии -> уводим в ПОТОК через
#      loop.run_in_executor. Поток блокируется, а event loop свободен.
#   2) CPU-BOUND вычисления -> поток не поможет (он держит GIL и грузит ядро),
#      нужен отдельный ПРОЦЕСС через ProcessPoolExecutor.
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

START = 0.0


def stamp() -> str:
    return f"[{time.perf_counter() - START:.2f}с]"


def blocking_io(seconds: float) -> str:
    # Представь, что это синхронная библиотека без async-версии (старый SDK,
    # legacy-клиент к БД и т.п.). Внутри -- блокирующий вызов.
    time.sleep(seconds)
    return f"блокирующая работа {seconds} с завершена"


def heavy_compute(n: int) -> int:
    # CPU-bound: реальные вычисления, никакого I/O. Такое держит GIL, и в потоке
    # event loop бы всё равно стоял -- поэтому уводим в отдельный процесс.
    total = 0
    for i in range(n):
        total += i * i
    return total


async def ticker(tag: str, n: int):
    for i in range(1, n + 1):
        print(f"  {stamp()} {tag} tick {i}")
        await asyncio.sleep(0.2)


async def main_thread():
    global START
    START = time.perf_counter()
    loop = asyncio.get_running_loop()
    ticks = asyncio.create_task(ticker("A", 12))
    # None = дефолтный ThreadPoolExecutor. Блокирующая функция уходит в поток,
    # await отдаёт управление loop'у -- тики продолжают идти во время ожидания.
    result = await loop.run_in_executor(None, blocking_io, 1.5)
    print(f"  {stamp()} результат из потока: {result}")
    await ticks


async def main_process():
    global START
    START = time.perf_counter()
    loop = asyncio.get_running_loop()
    ticks = asyncio.create_task(ticker("A", 20))
    # Тяжёлое вычисление уходит в ОТДЕЛЬНЫЙ ПРОЦЕСС -- свой интерпретатор, свой
    # GIL. Пока он считает на другом ядре, наш event loop свободен и тики идут.
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy_compute, 30_000_000)
    print(f"  {stamp()} результат из процесса: {result}")
    await ticks


def demo6():
    # Через main.py гоняем только безопасную часть с потоком -- она работает
    # везде. Часть с процессом требует прямого запуска файла (см. __main__ ниже).
    print("-- run_in_executor + поток: блокирующий вызов не вешает loop --")
    asyncio.run(main_thread())


if __name__ == "__main__":
    demo6()
    # ВАЖНО про ProcessPoolExecutor на Windows: дочерний процесс использует
    # spawn -- он ЗАНОВО импортирует этот модуль, чтобы найти heavy_compute.
    # Поэтому функция объявлена на верхнем уровне, а запуск -- под __main__.
    # Через importlib из main.py дочерний процесс модуль не нашёл бы, поэтому
    # process-часть гоняем только при прямом запуске: python 06_run_in_executor.py
    print("-- run_in_executor + процесс: CPU-bound не вешает loop --")
    asyncio.run(main_process())
