"""Эталонное решение практики 1 — сводка по тестам."""

test_results = [
    {"name": "test_login",   "status": "pass"},
    {"name": "test_logout",  "status": "fail"},
    {"name": "test_signup",  "status": "pass"},
    {"name": "test_payment", "status": "fail"},
    {"name": "test_profile", "status": "pass"},
]


def count_pass_fail(results):
    counts = {"pass": 0, "fail": 0}
    for case in results:
        status = case["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def filter_failed(results):
    return [case["name"] for case in results if case["status"] == "fail"]


def build_summary(results):
    counts = count_pass_fail(results)
    total = len(results)
    passed = counts["pass"]
    failed = counts["fail"]
    pass_rate = round(passed / total * 100) if total else 0
    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
    }


def format_summary(results):
    summary = build_summary(results)
    failed_names = filter_failed(results)

    lines = [
        "===== Сводка по тестам =====",
        f"Всего:  {summary['total']}",
        f"Прошло: {summary['passed']}",
        f"Упало:  {summary['failed']}",
        f"Успех:  {summary['pass_rate']}%",
    ]
    if failed_names:
        lines.append("Упавшие тесты:")
        for i, name in enumerate(failed_names, start=1):
            lines.append(f"  {i}. {name}")
    else:
        lines.append("Все тесты прошли!")
    return "\n".join(lines)


if __name__ == "__main__":
    print(format_summary(test_results))
