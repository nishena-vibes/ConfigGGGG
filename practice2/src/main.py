"""Визуализация графа зависимостей (этап 5)."""

import sys

from cli import parse_arguments, print_config, validate_arguments
from graph import bfs_build_graph
from order import load_order
from plantuml import generate_ascii_tree, generate_plantuml
from repo import fetch_dependencies
from test_repo import make_test_fetch_fn, parse_test_repo_file

LOAD_ORDER_NOTES = (
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

VISUALIZATION_NOTES = (
    "Сравнение со штатными инструментами визуализации Maven:\n"
    "1. Утилита генерирует PlantUML-описание графа, которое можно отрендерить\n"
    "   в любом PlantUML-совместимом инструменте.\n"
    "2. Maven не имеет встроенной графической визуализации графа;\n"
    "   `mvn dependency:tree` выводит текстовое дерево, а сторонние плагины\n"
    "   (напр. maven-dependency-graph) создают Graphviz/DOT файлы.\n"
    "3. Расхождение: PlantUML использует свой синтаксис диаграмм, а DOT —\n"
    "   свой. Утилита не скрывает и не дублирует версионные метки, тогда как\n"
    "   некоторые Maven-плагины могут показывать только координаты group:artifact\n"
    "   без версии. Это ожидаемое отличие при упрощённой реализации."
)


def main():
    """Точка входа приложения этапа 5."""
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

    print(f"PlantUML диаграмма графа зависимостей для {params['package']}:")
    print(generate_plantuml(graph))

    if params["ascii_tree"]:
        print(f"ASCII-дерево зависимостей для {params['package']}:")
        print(generate_ascii_tree(graph, params["package"]))
        print()

    if params["load_order"]:
        order = load_order(graph, params["package"])
        print(f"Порядок загрузки для {params['package']}:")
        for idx, package in enumerate(order, 1):
            print(f"{idx}. {package}")
        print()
    elif not params["ascii_tree"]:
        print(f"Граф зависимостей для {params['package']}:")
        for package in sorted(graph.all_packages()):
            deps = sorted(graph.neighbors(package))
            deps_str = ", ".join(deps) if deps else ""
            print(f"{package} -> {deps_str}")
        print()

    print(LOAD_ORDER_NOTES)
    print()
    print(VISUALIZATION_NOTES)


def _make_real_fetch_fn(repo_url):
    """Создать функцию получения зависимостей из реального репозитория."""

    def fetch(package):
        return fetch_dependencies(repo_url, package)

    return fetch


if __name__ == "__main__":
    main()
