# Урок B1.3 -- Главная ловушка: блокирующий вызов вешает весь event loop
#
# await asyncio.sleep(x) отдаёт управление loop'у -- другие корутины работают.
# time.sleep(x) -- синхронный блокирующий вызов: поток стоит внутри C-функции,
# loop не получает управление и НЕ МОЖЕТ переключиться. Один такой вызов в
# async-коде замораживает ВСЁ приложение на это время.
import asyncio
import time

START = 0.0


def stamp() -> str:
    return f"[{time.perf_counter() - START:.2f}с]"


async def ticker(tag: str):
    # "Пульс" приложения: тик каждые 0.2 с. Пока тики идут ровно -- event loop
    # жив и переключается. Замерли тики -- значит loop кем-то заблокирован.
    for i in range(1, 11):
        await asyncio.sleep(0.2)
        print(f"  {stamp()} {tag} tick {i}")


async def good_worker():
    print(f"  {stamp()} good_worker: начал, впереди await asyncio.sleep(1)")
    await asyncio.sleep(1.0)                # НЕблокирующее ожидание -- loop свободен
    print(f"  {stamp()} good_worker: проснулся")


async def bad_worker():
    print(f"  {stamp()} bad_worker: начал, впереди time.sleep(1) [БЛОКИРУЕТ]")
    time.sleep(1.0)                         # БЛОКИРУЮЩИЙ вызов -- loop стоит секунду
    print(f"  {stamp()} bad_worker: проснулся")


async def main_good():
    global START
    START = time.perf_counter()
    await asyncio.gather(ticker("A"), good_worker())


async def main_bad():
    global START
    START = time.perf_counter()
    await asyncio.gather(ticker("A"), bad_worker())


def demo3():
    print("-- ПРАВИЛЬНО: await asyncio.sleep -- тики идут ровно, loop жив --")
    asyncio.run(main_good())
    print("-- НЕПРАВИЛЬНО: time.sleep внутри async -- тики замирают на 1 с --")
    print("  (смотри на паузу в метках времени: loop заблокирован)")
    asyncio.run(main_bad())


if __name__ == "__main__":
    demo3()
