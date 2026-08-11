# Урок B1.5 -- ГЛАВНОЕ ДЕМО: запрос к сайту ПАРАЛЛЕЛЬНО с тиками в консоль
#
# Запускаем две корутины конкурентно:
#   blinker()  -- печатает "tick" каждые 0.3 с (работа, которая идёт, пока
#                 мы ждём сеть);
#   download() -- делает GET на медленную страницу через aiohttp.
#
# Что ты увидишь: download стартует, упирается в await на ответ сервера и
# ОТДАЁТ управление loop'у. Пока сокет ждёт данные (он зарегистрирован в epoll/
# selector), loop крутит blinker и печатает тики. Как только страница отдалась --
# ОС будит сокет, loop ВОЗОБНОВЛЯЕТ download ровно с того же await, и он
# допечатывает результат. Вот он, контекст-свитч, вживую.
import asyncio
import time

import aiohttp

START = 0.0


def stamp() -> str:
    return f"[{time.perf_counter() - START:.2f}с]"


# Медленная страница: сервер отвечает через 3 секунды. За это время loop
# успеет напечатать примерно 10 тиков.
SLOW_URL = "https://httpbin.org/delay/3"


async def blinker():
    i = 0
    while True:
        i += 1
        print(f"  {stamp()} tick {i}   <- loop свободен, пока сокет ждёт ответ")
        await asyncio.sleep(0.3)


async def download(url: str) -> int:
    print(f"  {stamp()} download: открываю соединение с {url}")
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        print(f"  {stamp()} download: запрос отправлен, впереди await ответа сервера")
        async with session.get(url) as response:
            print(f"  {stamp()} download: пришли заголовки, статус {response.status}")
            body = await response.read()    # ждём тело страницы
    print(f"  {stamp()} download: страница получена, {len(body)} байт  <<< КОНТЕКСТ ВЕРНУЛСЯ СЮДА")
    return len(body)


async def main():
    global START
    START = time.perf_counter()
    # blinker бесконечный -- запускаем его как фоновую задачу и гасим, когда
    # download закончился.
    ticks = asyncio.create_task(blinker())
    try:
        await download(SLOW_URL)
    finally:
        ticks.cancel()                      # останавливаем тики
        try:
            await ticks                     # даём отмене корректно завершиться
        except asyncio.CancelledError:
            pass
    print(f"  {stamp()} готово")


def demo5():
    print("-- запрос к сайту идёт ПАРАЛЛЕЛЬНО с тиками в консоль --")
    print("  [нужен интернет; сервер отвечает через ~3 с -- считай тики между стартом и ответом]")
    try:
        asyncio.run(main())
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"  сеть недоступна или сервер не ответил: {e!r}")


if __name__ == "__main__":
    demo5()
