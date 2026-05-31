"""
ПРАКТИКА 1 — Сводка по результатам тестов.

Дан список тест-кейсов, у каждого имя и статус ("pass" / "fail").
Реализуй функции ниже (убери `pass` и напиши код). Затем запусти файл:

    python practice_test_report.py

Внизу есть простой self-check, который скажет, что работает, а что нет.
Эталон: solutions/practice_test_report_solution.py
"""

test_results = [
    {"name": "test_login",   "status": "pass"},
    {"name": "test_logout",  "status": "fail"},
    {"name": "test_signup",  "status": "pass"},
    {"name": "test_payment", "status": "fail"},
    {"name": "test_profile", "status": "pass"},
]


def count_pass_fail(results):
    """Вернуть словарь {"pass": N, "fail": M}."""
    pass  # TODO


def filter_failed(results):
    """Вернуть список ИМЁН упавших тестов."""
    pass  # TODO


def build_summary(results):
    """Вернуть сводку:
    {"total": ..., "passed": ..., "failed": ..., "pass_rate": ...}
    pass_rate — процент пройденных, округлённый до целого (round()).
    Не забудь про пустой список: деления на ноль быть не должно."""
    pass  # TODO


def format_summary(results):
    """Вернуть многострочную строку-отчёт для печати в консоль.
    Покажи всего/прошло/упало/процент и перечисли упавшие тесты"""
    pass  # TODO


# ── простой self-check ──────────────────────────────────────────────────────

def _check(name, got, expected):
    mark = "OK  " if got == expected else "FAIL"
    print(f"[{mark}] {name}")
    if got != expected:
        print(f"       ожидалось: {expected!r}")
        print(f"       получено:  {got!r}")


if __name__ == "__main__":
    _check("count_pass_fail", count_pass_fail(test_results),
           {"pass": 3, "fail": 2})
    _check("filter_failed", filter_failed(test_results),
           ["test_logout", "test_payment"])
    _check("build_summary", build_summary(test_results),
           {"total": 5, "passed": 3, "failed": 2, "pass_rate": 60})
    _check("build_summary (пустой)", build_summary([]),
           {"total": 0, "passed": 0, "failed": 0, "pass_rate": 0})

    print()
    print(format_summary(test_results))
