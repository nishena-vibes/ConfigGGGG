"""Парсинг и валидация параметров командной строки (этап 1)."""

import argparse
import sys


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей Maven"
    )
    args_spec = [
        ("--package", {"type": str, "default": None,
                       "help": "Имя анализируемого пакета"}),
        ("--repo", {"type": str, "default": None,
                    "help": "URL репозитория или путь к файлу тестового репозитория"}),
        ("--test-repo", {"action": "store_true", "default": False,
                         "help": "Режим работы с тестовым репозиторием"}),
        ("--ascii-tree", {"action": "store_true", "default": False,
                          "help": "Вывод зависимостей в виде ASCII-дерева"}),
        ("--max-depth", {"type": int, "default": None,
                         "help": "Максимальная глубина анализа зависимостей"}),
        ("--filter", {"type": str, "default": None,
                      "help": "Подстрока для фильтрации пакетов"}),
        ("--load-order", {"action": "store_true", "default": False,
                          "help": "Вывод порядка загрузки зависимостей"}),
    ]
    for name, kwargs in args_spec:
        parser.add_argument(name, **kwargs)
    return parser.parse_args()


def _required_string(value, name):
    """Возвращает (строка, None) или (None, сообщение об ошибке)."""
    if not value or not value.strip():
        return None, f"{name}: не задан или пустой"
    return value.strip(), None


def _add_error(errors, message):
    errors.append(message)


def _validate_required(value, name, params, errors):
    result, err = _required_string(value, name)
    if err:
        _add_error(errors, err)
    else:
        params[name] = result


def _validate_max_depth(value, params, errors):
    if value is None:
        _add_error(errors, "max-depth: не задан")
    elif value < 1:
        _add_error(errors, "max-depth: должно быть целым числом >= 1")
    else:
        params["max_depth"] = value


def _validate_filter(value, params, errors):
    if value is not None and not isinstance(value, str):
        _add_error(errors, "filter: должно быть строкой")
    else:
        params["filter"] = value


def _raise_if_errors(errors):
    if errors:
        for error in errors:
            print(f"Error: {error}")
        sys.exit(1)


def validate_arguments(args):
    """Проверяет все параметры и возвращает словарь параметров.
    При некорректном значении любого параметра печатает ошибку и
    завершает программу с кодом 1.
    """
    params = {}
    errors = []

    _validate_required(args.package, "package", params, errors)
    _validate_required(args.repo, "repo", params, errors)

    params.update(test_repo=bool(args.test_repo), ascii_tree=bool(args.ascii_tree),
                  load_order=bool(args.load_order))

    _validate_max_depth(args.max_depth, params, errors)
    _validate_filter(args.filter, params, errors)

    _raise_if_errors(errors)

    return params


def print_config(params):
    """Печатает все настраиваемые параметры в формате ключ=значение."""
    for key in sorted(params):
        print(f"{key}={params[key]}")
