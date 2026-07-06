# Урок B6.4 -- Синхронный запрос (requests) против асинхронного (aiohttp)
#
# Один и тот же список URL качаем двумя способами:
#   requests -- ПОСЛЕДОВАТЕЛЬНО: суммарное время ~= сумма всех задержек;
#   aiohttp  -- КОНКУРЕНТНО:     суммарное время ~= САМАЯ ДОЛГАЯ задержка.
# Разница не в "скорости библиотеки", а в том, что пока один запрос ждёт ответ
# сервера, event loop успевает отправить и ждать остальные -- на одном потоке.
import asyncio
import time

import aiohttp
import requests


# httpbin.org/delay/N отвечает через N секунд -- удобно для наглядности.
# Нет интернета или httpbin молчит -- подставь любой набор реальных URL.
URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
]


def fetch_sync(url: str) -> int:
    response = requests.get(url, timeout=30)
    return len(response.content)


def run_sync():
    start = time.perf_counter()
    sizes = [fetch_sync(url) for url in URLS]        # строго по очереди
    elapsed = time.perf_counter() - start
    print(f"  requests (последовательно): {elapsed:.2f} с | байт: {sizes}")


async def fetch_async(session: aiohttp.ClientSession, url: str) -> int:
    # await в двух местах: пока идёт запрос и пока читается тело -- управление
    # уходит в loop, и он в это время занимается остальными запросами.
    async with session.get(url) as response:
        body = await response.read()
        return len(body)


async def run_async():
    start = time.perf_counter()
    timeout = aiohttp.ClientTimeout(total=30)
    # Одна ClientSession на все запросы -- переиспользует пул соединений.
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # gather запускает все запросы конкурентно на ОДНОМ потоке.
        sizes = await asyncio.gather(*(fetch_async(session, url) for url in URLS))
    elapsed = time.perf_counter() - start
    print(f"  aiohttp  (конкурентно):     {elapsed:.2f} с | байт: {sizes}")


def demo4():
    print("-- качаем 4 URL (задержки 1+2+1+2 = 6 с суммарно) --")
    print("  [нужен интернет; если httpbin молчит -- поменяй URLS]")
    try:
        run_sync()                          # ~6 с
        asyncio.run(run_async())            # ~2 с (самая долгая задержка)
    except (requests.RequestException, aiohttp.ClientError, asyncio.TimeoutError) as e:
        print(f"  сеть недоступна или сервер не ответил: {e!r}")


if __name__ == "__main__":
    demo4()
