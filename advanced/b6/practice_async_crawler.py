"""
Урок B6 -- ПРАКТИЧЕСКАЯ РАБОТА
Асинхронный чекер сайтов: проверяем пачку URL КОНКУРЕНТНО на aiohttp и
сравниваем со старым синхронным подходом на requests.

Идея проекта: есть список URL. Для каждого нужно узнать HTTP-статус, размер
ответа и сколько секунд занял запрос. Синхронно (requests) это тянется по
очереди -- суммарное время складывается. Асинхронно (aiohttp) все запросы
летят конкурентно на одном потоке -- общее время падает до самого долгого
ответа. Твоя задача -- написать асинхронную версию и увидеть разницу вживую.

Тебе ДАНЫ: список URL, синхронная эталонная функция check_all_sync (baseline)
и заготовка demo(). Писать нужно async-часть.


====================================================================
ШАГ 0. Разведка
--------------------------------------------------------------------
Запусти файл как есть: python practice_async_crawler.py -- отработает только
синхронный baseline (по очереди, медленно). Засеки суммарное время: оно
примерно равно СУММЕ задержек всех URL. Твоя async-версия должна уложиться
примерно в САМУЮ ДОЛГУЮ задержку.


====================================================================
ШАГ 1. Корутина check(session, url, semaphore)
--------------------------------------------------------------------
Проверяет ОДИН url. Принимает готовую aiohttp.ClientSession (не создавай
сессию внутри -- одна на всех, см. ШАГ 2) и asyncio.Semaphore. Поведение:

  - под `async with semaphore:` (ограничиваем число одновременных запросов),
  - засечь время (time.perf_counter),
  - `async with session.get(url) as response:` -- сделать запрос,
  - прочитать тело `await response.read()` (нужен размер),
  - вернуть dict: {"url": url, "status": response.status,
                   "size": <байт>, "elapsed": <сек, round(..., 2)>}.

Ошибки НЕ должны ронять весь чекер: оберни в try/except и на
aiohttp.ClientError / asyncio.TimeoutError верни
  {"url": url, "status": "error", "size": 0, "elapsed": ...,
   "detail": repr(e)}.


====================================================================
ШАГ 2. Корутина check_all_async(urls, limit=5)
--------------------------------------------------------------------
  - создать ОДНУ сессию: `async with aiohttp.ClientSession(timeout=...) as session:`
    (timeout = aiohttp.ClientTimeout(total=20)) -- она переиспользует
    пул соединений, поднимать по сессии на запрос -- антипаттерн;
  - создать `semaphore = asyncio.Semaphore(limit)` -- не больше `limit`
    запросов в полёте одновременно (вежливость к серверу и к своей сети);
  - собрать задачи и запустить их КОНКУРЕНТНО через asyncio.gather;
  - вернуть список результатов.

Почему семафор, а не просто gather на 1000 URL: 1000 одновременных сокетов
могут упереться в лимиты ОС/сервера. Семафор -- это "пропускаем по limit за
раз", классический приём backpressure в async.


====================================================================
ШАГ 3. demo()
--------------------------------------------------------------------
  1. Прогнать check_all_sync(URLS), напечатать суммарное время.
  2. Прогнать asyncio.run(check_all_async(URLS)), напечатать суммарное время.
  3. Напечатать результаты async-версии построчно (url -> status, size, elapsed).
  4. Вывести ускорение: sync_time / async_time (во сколько раз быстрее).

Ожидаемо: sync ~= сумма задержек, async ~= самая долгая задержка.


====================================================================
СО ЗВЁЗДОЧКОЙ (по желанию)
--------------------------------------------------------------------
  - as_completed: печатай результат каждого URL СРАЗУ, как он готов, а не
    дожидаясь всех (asyncio.as_completed вместо gather).
  - Ретраи: оберни check в повтор на 2-3 попытки при таймауте (вспомни @retry
    из B3, только теперь с await asyncio.sleep между попытками).
  - Замерь, как меняется общее время при limit=1, 2, 5, 20 -- и объясни почему.
"""

import asyncio
import time

import aiohttp
import requests


# Смесь задержек, чтобы разница sync/async была очевидна.
# httpbin.org/delay/N отвечает через N секунд.
URLS = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/200",
]


def check_sync(url: str) -> dict:
    """Синхронная проверка одного URL -- эталон для сравнения (уже знаком по B3)."""
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=20)
        return {
            "url": url,
            "status": response.status_code,
            "size": len(response.content),
            "elapsed": round(time.perf_counter() - start, 2),
        }
    except requests.RequestException as e:
        return {"url": url, "status": "error", "size": 0,
                "elapsed": round(time.perf_counter() - start, 2), "detail": repr(e)}


def check_all_sync(urls: list[str]) -> list[dict]:
    """Baseline: строго по очереди. Суммарное время ~= сумма задержек."""
    return [check_sync(url) for url in urls]


# ------------------------------------------------------------------
# ТВОЙ КОД НИЖЕ. Заготовки бросают NotImplementedError -- замени телом.
# ------------------------------------------------------------------

async def check(session: aiohttp.ClientSession, url: str,
                semaphore: asyncio.Semaphore) -> dict:
    raise NotImplementedError("ШАГ 1: реализуй проверку одного URL через aiohttp")


async def check_all_async(urls: list[str], limit: int = 5) -> list[dict]:
    raise NotImplementedError("ШАГ 2: одна сессия + семафор + gather")


def demo():
    print("== СИНХРОННО (requests, по очереди) ==")
    start = time.perf_counter()
    sync_results = check_all_sync(URLS)
    sync_time = time.perf_counter() - start
    print(f"  время: {sync_time:.2f} с")

    print("== АСИНХРОННО (aiohttp, конкурентно) ==")
    start = time.perf_counter()
    async_results = asyncio.run(check_all_async(URLS))
    async_time = time.perf_counter() - start
    print(f"  время: {async_time:.2f} с")
    for r in async_results:
        print(f"  {r['url']} -> status={r['status']}, "
              f"size={r['size']}, elapsed={r['elapsed']}с")

    if async_time > 0:
        print(f"== ускорение: в {sync_time / async_time:.1f} раз быстрее ==")


if __name__ == "__main__":
    # Пока не реализованы check/check_all_async -- упадёт на NotImplementedError.
    # Реализуй ШАГИ 1-3 и запусти снова.
    demo()
