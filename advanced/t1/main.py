import importlib.util
from pathlib import Path


def _load(filename: str):
    """Файлы начинаются с цифры — обычным import их не подключить.
    Грузим модуль напрямую по пути через importlib."""
    path = Path(__file__).parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Раскомментируй нужную строку и запусти: python main.py

_load("01_loops.py").demo1()            # for / while / range / break / continue / for-else
# _load("02_enumerate_zip.py").demo2()  # enumerate и zip
# _load("03_lists.py").demo3()          # списки: методы и срезы
# _load("04_comprehensions.py").demo4() # генераторы списков
# _load("05_collections.py").demo5()    # кортежи, множества, словари

# --- Практику запускай напрямую: ---
#   python practice_test_report.py
#   python practice_leetcode.py
