"""Парсинг и валидация параметров командной строки (этап 1)."""

import argparse
import sys


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей Maven"
    )
    parser.add_argument(
        "--package",
        type=str,
        default=None,
        help="Имя анализируемого пакета",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="URL репозитория или путь к файлу тестового репозитория",
    )
    parser.add_argument(
        "--test-repo",
        action="store_true",
        default=False,
        help="Режим работы с тестовым репозиторием",
    )
    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        default=False,
        help="Вывод зависимостей в виде ASCII-дерева",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=None,
        help="Максимальная глубина анализа зависимостей",
    )
    parser.add_argument(
        "--filter",
        type=str,
        default=None,
        help="Подстрока для фильтрации пакетов",
    )
    parser.add_argument(
        "--load-order",
        action="store_true",
        default=False,
        help="Вывод порядка загрузки зависимостей",
    )
    return parser.parse_args()


def validate_arguments(args):
    """Проверяет все параметры и возвращает словарь параметров.

    При некорректном значении любого параметра печатает ошибку и
    завершает программу с кодом 1.
    """
    params = {}
    errors = []

    package = args.package
    if not package or not package.strip():
        errors.append("package: не задан или пустой")
    else:
        params["package"] = package.strip()

    repo = args.repo
    if not repo or not repo.strip():
        errors.append("repo: не задан или пустой")
    else:
        params["repo"] = repo.strip()

    params["test_repo"] = bool(args.test_repo)
    params["ascii_tree"] = bool(args.ascii_tree)
    params["load_order"] = bool(args.load_order)

    max_depth = args.max_depth
    if max_depth is None:
        errors.append("max-depth: не задан")
    elif max_depth < 1:
        errors.append("max-depth: должно быть целым числом >= 1")
    else:
        params["max_depth"] = max_depth

    filter_sub = args.filter
    if filter_sub is not None and not isinstance(filter_sub, str):
        errors.append("filter: должно быть строкой")
    else:
        params["filter"] = filter_sub

    if errors:
        for error in errors:
            print(f"Error: {error}")
        sys.exit(1)

    return params


def print_config(params):
    """Печатает все настраиваемые параметры в формате ключ=значение."""
    for key in sorted(params):
        print(f"{key}={params[key]}")
