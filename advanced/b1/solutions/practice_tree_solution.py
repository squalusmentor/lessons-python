"""
Урок B1 — РЕШЕНИЕ практической работы 2 (свой аналог tree).

Две версии:
  - print_tree_simple — базовая, отступ пробелами (как в условии);
  - print_tree        — "настоящая", с рамками ├── └── │.

Запуск:  python solutions/practice_tree_solution.py
"""

from pathlib import Path


# Шум вроде __pycache__ и скрытых папок (.git, .claude) в дерево не пускаем.
def _visible(entries):
    return [e for e in entries if e.name != "__pycache__" and not e.name.startswith(".")]


# --- Базовая версия: отступ пробелами ---
def print_tree_simple(path: Path, depth: int = 0) -> None:
    suffix = "/" if path.is_dir() else ""
    print("    " * depth + path.name + suffix)   # печатаем текущий элемент
    if path.is_dir():                            # ШАГ: углубляемся в директорию
        for entry in _visible(sorted(path.iterdir())):
            print_tree_simple(entry, depth + 1)
    # БАЗА: для файла is_dir() ложно — рекурсия просто не идёт дальше.


# --- Версия с рамками, как настоящий tree ---
def print_tree(path: Path) -> None:
    print(path.name + ("/" if path.is_dir() else ""))   # корень
    _walk(path, "")


def _walk(path: Path, prefix: str) -> None:
    if not path.is_dir():            # БАЗА: файл — детей нет
        return
    entries = _visible(sorted(path.iterdir()))
    for i, entry in enumerate(entries):
        last = (i == len(entries) - 1)
        connector = "└── " if last else "├── "
        print(prefix + connector + entry.name + ("/" if entry.is_dir() else ""))
        # вертикальную черту продолжаем только если ниже ещё есть соседи
        extension = "    " if last else "│   "
        _walk(entry, prefix + extension)   # ШАГ


def demo_tree():
    here = Path(__file__).parent.parent   # папка урока b1

    print("== Версия 1: отступ пробелами ==")
    print_tree_simple(here)

    print("\n== Версия 2: рамки ├── └── ==")
    print_tree(here)


if __name__ == "__main__":
    demo_tree()
