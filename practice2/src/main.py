"""Построение графа зависимостей (этап 3)."""

import sys

from cli import parse_arguments, print_config, validate_arguments
from graph import bfs_build_graph
from repo import fetch_dependencies
from test_repo import make_test_fetch_fn, parse_test_repo_file


def main():
    """Точка входа приложения этапа 3."""
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

    print(f"Граф зависимостей для {params['package']}:")
    for package in sorted(graph.all_packages()):
        deps = sorted(graph.neighbors(package))
        deps_str = ", ".join(deps) if deps else ""
        print(f"{package} -> {deps_str}")


def _make_real_fetch_fn(repo_url):
    """Создать функцию получения зависимостей из реального репозитория."""

    def fetch(package):
        return fetch_dependencies(repo_url, package)

    return fetch


if __name__ == "__main__":
    main()
