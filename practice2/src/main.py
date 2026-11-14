"""Сбор данных о прямых зависимостях Maven-пакета (этап 2)."""

import sys

from cli import parse_arguments, print_config, validate_arguments
from repo import fetch_dependencies


def main():
    """Точка входа приложения этапа 2."""
    args = parse_arguments()
    params = validate_arguments(args)
    print_config(params)
    dependencies = fetch_dependencies(params["repo"], params["package"])
    if not dependencies:
        print(f"Прямые зависимости для {params['package']} не найдены")
        return
    print(f"Прямые зависимости для {params['package']}:")
    for dep in sorted(dependencies):
        print(dep)


if __name__ == "__main__":
    main()
