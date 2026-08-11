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


# Раскомментируй нужный блок и запусти: python main.py

# --- Блок 1. Функции вглубь ---
_load("01_args_kwargs.py").demo1()      # *args / **kwargs
# _load("02_scope.py").demo2()          # область видимости (LEGB)
# _load("03_closures.py").demo3()       # замыкания
# _load("04_first_class.py").demo4()    # функции как объекты первого класса

# --- Блок 2. Рекурсия ---
# _load("05_recursion.py").demo5()      # рекурсия
# _load("06_recursion_tasks.py").demo6()  # задачи на рекурсию (стабы)

# --- Практика: смотри to-do.md ---
