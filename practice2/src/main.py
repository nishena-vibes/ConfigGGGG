"""Дополнительные операции над графом зависимостей (этап 4)."""

import sys

from cli import parse_arguments, print_config, validate_arguments
from graph import bfs_build_graph
from order import load_order
from repo import fetch_dependencies
from test_repo import make_test_fetch_fn, parse_test_repo_file

COMPARISON_NOTES = (
    "Сравнение со штатным менеджером пакетов (Maven):\n"
    "1. Утилита учитывает только прямые и транзитивные зависимости из POM.\n"
    "2. Maven дополнительно применяет dependencyManagement, исключения\n"
    "   (exclusions), optional зависимости, области видимости (scope) и\n"
    "   медиацию версий (поближайшее определение выигрывает), что может\n"
    "   изменить порядок загрузки и состав пакетов.\n"
    "3. Результат утилиты может отличаться от Maven из-за отсутствия\n"
    "   вышеуказанной логики — это ожидаемое расхождение при упрощённой\n"
    "   реализации."
)


def main():
    """Точка входа приложения этапа 4."""
    args = parse_arguments()
    params = validate_arguments(args)
    print_config(params)

    if params["test_repo"]:
        graph_data = parse_test_repo_file(params["repo"])
        fetch_fn = make_test_fetch_fn(graph_data)
    else:
        fetch_fn = _make_real_fetch_fn(params["repo"])

    graph = bfs_build_graph(
        fetch_fn,
        params["package"],
        params["max_depth"],
        params["filter"],
    )

    if not graph.all_packages():
        print(f"Зависимости для {params['package']} не найдены")
        return

    if params["load_order"]:
        order = load_order(graph, params["package"])
        print(f"Порядок загрузки для {params['package']}:")
        for idx, package in enumerate(order, 1):
            print(f"{idx}. {package}")
    else:
        print(f"Граф зависимостей для {params['package']}:")
        for package in sorted(graph.all_packages()):
            deps = sorted(graph.neighbors(package))
            deps_str = ", ".join(deps) if deps else ""
            print(f"{package} -> {deps_str}")

    print()
    print(COMPARISON_NOTES)


def _make_real_fetch_fn(repo_url):
    """Создать функцию получения зависимостей из реального репозитория."""

    def fetch(package):
        return fetch_dependencies(repo_url, package)

    return fetch


if __name__ == "__main__":
    main()
