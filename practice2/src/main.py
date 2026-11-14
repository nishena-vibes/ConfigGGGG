"""Минимальный прототип CLI с конфигурацией (этап 1)."""

from cli import parse_arguments, print_config, validate_arguments


def main():
    """Точка входа приложения этапа 1."""
    args = parse_arguments()
    params = validate_arguments(args)
    print_config(params)


if __name__ == "__main__":
    main()
