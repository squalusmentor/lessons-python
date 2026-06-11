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

# --- Блок 1. Декораторы ---
_load("01_nested_functions.py").demo1()     # вложенные функции и замыкания
# _load("02_own_decorators.py").demo2()     # свои декораторы: функции и методы
# _load("03_params_wraps.py").demo3()       # параметры декоратора, functools.wraps
# _load("04_real_decorators.py").demo4()    # рабочие @timer, @retry, @cache

# --- Блок 2. Парсинг HTML ---
# _load("05_bs4.py").demo5()                # BeautifulSoup: селекторы и атрибуты

# --- Практику запускай напрямую: ---
#   python practice_kovrov_news.py
