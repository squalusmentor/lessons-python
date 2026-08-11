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

# --- Занятие 1. Инкапсуляция, наследование, полиморфизм, dunder ---
_load("01_classes_encapsulation.py").demo1()        # классы и инкапсуляция
# _load("02_inheritance.py").demo2()                # наследование, super()
# _load("03_polymorphism.py").demo3()               # полиморфизм и утиная типизация
# _load("04_dunder.py").demo4()                     # dunder-методы

# --- Занятие 2. property, композиция vs наследование, паттерны ---
# _load("05_property.py").demo5()                   # property
# _load("06_composition_vs_inheritance.py").demo6() # композиция против наследования
# _load("07_patterns.py").demo7()                   # паттерны: фабрика, синглтон

# --- Практика: смотри to-do.md ---
