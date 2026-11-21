"""Визуализация графа зависимостей (этап 5)."""

import sys

from cli import parse_arguments, print_config, validate_arguments
from graph import bfs_build_graph
from order import load_order
from plantuml import generate_ascii_tree, generate_plantuml
from repo import fetch_dependencies
from test_repo import make_test_fetch_fn, parse_test_repo_file


def main():
    """Точка входа приложения этапа 5."""
    args = parse_arguments()
    params = validate_arguments(args)
    # print_config(params) # Was used for part1

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


def _make_real_fetch_fn(repo_url):
    """Создать функцию получения зависимостей из реального репозитория."""

    def fetch(package):
        return fetch_dependencies(repo_url, package)

    return fetch


if __name__ == "__main__":
    main()
