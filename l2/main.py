import importlib.util
from pathlib import Path


def _load(filename: str):
    """Имена файлов начинаются с цифры, обычным import их не подключить —
    используем importlib, чтобы загрузить модуль напрямую по пути."""
    path = Path(__file__).parent / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Раскомментируй нужный блок и запусти: python main.py

# _load("01_conditions.py").demo1()  # условия
_load("02_loops.py").demo2()         # циклы
# _load("03_functions.py").demo3()   # функции
# _load("04_practice.py").demo4()    # практика
