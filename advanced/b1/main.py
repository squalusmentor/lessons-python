import importlib.util
from pathlib import Path


def _load(filename: str):
    """Файлы начинаются с цифры -- обычным import их не подключить.
    Грузим модуль напрямую по пути через importlib."""
    path = Path(__file__).parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Раскомментируй нужную строку и запусти: python main.py

# --- Блок 1. Основы asyncio (сеть не нужна) ---
_load("01_coroutines.py").demo1()            # корутины, await, asyncio.run
# _load("02_event_loop.py").demo2()          # event loop: sequential vs gather, create_task
# _load("03_blocking_vs_await.py").demo3()   # ловушка: time.sleep вешает весь loop

# --- Блок 2. Асинхронный I/O на aiohttp (нужен интернет) ---
# _load("04_sync_vs_async_requests.py").demo4()      # requests против aiohttp: замер времени
# _load("05_parallel_request_and_ticks.py").demo5()  # запрос к сайту параллельно с тиками
# _load("06_run_in_executor.py").demo6()             # run_in_executor: поток (и процесс)

# --- Практика: смотри to-do.md ---
