"""Тесты валидации параметров CLI (этап 1)."""

import sys
import unittest

sys.path.insert(0, "src")

from cli import validate_arguments


class FakeArgs:
    """Заглушка аргументов argparse для тестов."""

    def __init__(
        self,
        package,
        repo,
        test_repo,
        ascii_tree,
        max_depth,
        filter_sub,
        load_order,
    ):
        self.package = package
        self.repo = repo
        self.test_repo = test_repo
        self.ascii_tree = ascii_tree
        self.max_depth = max_depth
        self.filter = filter_sub
        self.load_order = load_order


class TestValidateArguments(unittest.TestCase):
    """Тесты функции validate_arguments."""

    def test_valid_params(self):
        """Все параметры корректны -> возвращается словарь."""
        args = FakeArgs(
            "org.example:lib",
            "https://repo.example.com",
            False,
            False,
            3,
            "org",
            False,
        )
        params = validate_arguments(args)
        self.assertEqual(params["package"], "org.example:lib")
        self.assertEqual(params["repo"], "https://repo.example.com")
        self.assertEqual(params["max_depth"], 3)
        self.assertEqual(params["filter"], "org")
        self.assertEqual(params["load_order"], False)

    def test_empty_package(self):
        """Пустой пакет -> ошибка и выход с кодом 1."""
        args = FakeArgs(
            "", "https://repo.example.com", False, False, 3, None, False
        )
        with self.assertRaises(SystemExit) as ctx:
            validate_arguments(args)
        self.assertEqual(ctx.exception.code, 1)

    def test_negative_max_depth(self):
        """Отрицательная глубина -> ошибка."""
        args = FakeArgs(
            "pkg", "https://repo.example.com", False, False, -1, None, False
        )
        with self.assertRaises(SystemExit):
            validate_arguments(args)


if __name__ == "__main__":
    unittest.main()
