"""Тесты графа зависимостей и тестового репозитория (этап 3)."""

import sys
import unittest

sys.path.insert(0, "src")

from graph import bfs_build_graph, DependencyGraph, normalize_package
from test_repo import make_test_fetch_fn, parse_test_repo_file


class FixedDepthError(Exception):
    pass


class TestDependencyGraph(unittest.TestCase):
    """Тесты класса DependencyGraph."""

    def test_add_edge_and_neighbors(self):
        """Добавление ребра и получение соседей."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        self.assertEqual(graph.neighbors("A"), {"B", "C"})
        self.assertEqual(graph.neighbors("B"), set())

    def test_all_packages(self):
        """Все пакеты включают родителей и детей."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        self.assertEqual(graph.all_packages(), {"A", "B", "C"})


class TestBfsBuildGraph(unittest.TestCase):
    """Тесты рекурсивного BFS построения графа."""

    def test_linear_chain(self):
        """Линейная цепочка A -> B -> C."""
        graph_data = {"A": ["B"], "B": ["C"], "C": []}
        fetch_fn = make_test_fetch_fn(graph_data)
        graph = bfs_build_graph(fetch_fn, "A", max_depth=10)
        self.assertEqual(graph.neighbors("A"), {"B"})
        self.assertEqual(graph.neighbors("B"), {"C"})
        self.assertEqual(graph.neighbors("C"), set())

    def test_max_depth_limit(self):
        """Максимальная глубина ограничивает обход."""
        graph_data = {"A": ["B"], "B": ["C"], "C": []}
        fetch_fn = make_test_fetch_fn(graph_data)
        graph = bfs_build_graph(fetch_fn, "A", max_depth=1)
        self.assertEqual(graph.neighbors("A"), {"B"})
        self.assertEqual(graph.neighbors("B"), set())

    def test_cycle_handling(self):
        """Циклические зависимости не вызывают бесконечной рекурсии."""
        graph_data = {"A": ["B"], "B": ["C"], "C": ["A"]}
        fetch_fn = make_test_fetch_fn(graph_data)
        graph = bfs_build_graph(fetch_fn, "A", max_depth=10)
        self.assertEqual(graph.neighbors("A"), {"B"})
        self.assertEqual(graph.neighbors("B"), {"C"})
        self.assertEqual(graph.neighbors("C"), {"A"})

    def test_filter_substring(self):
        """Пакеты, содержащие подстроку фильтра, исключаются."""
        graph_data = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        fetch_fn = make_test_fetch_fn(graph_data)
        graph = bfs_build_graph(fetch_fn, "A", max_depth=10,
                                filter_substring="C")
        self.assertEqual(graph.neighbors("A"), {"B"})
        self.assertNotIn("C", graph.all_packages())

    def test_diamond_shared_dependency(self):
        """Алмазная зависимость: два пути к одному пакету."""
        graph_data = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        fetch_fn = make_test_fetch_fn(graph_data)
        graph = bfs_build_graph(fetch_fn, "A", max_depth=10)
        self.assertEqual(graph.neighbors("A"), {"B", "C"})
        self.assertEqual(graph.neighbors("B"), {"D"})
        self.assertEqual(graph.neighbors("C"), {"D"})
        self.assertIn("D", graph.all_packages())


class TestNormalizePackage(unittest.TestCase):
    """Тесты нормализации имён пакетов."""

    def test_full_coordinates(self):
        """group:artifact:version -> group:artifact."""
        self.assertEqual(normalize_package("org.example:lib:1.2"),
                         "org.example:lib")

    def test_without_version(self):
        """group:artifact остаётся без изменений."""
        self.assertEqual(normalize_package("org.example:lib"),
                         "org.example:lib")

    def test_single_token(self):
        """Один токен (тестовый пакет) остаётся без изменений."""
        self.assertEqual(normalize_package("A"), "A")


class TestParseTestRepoFile(unittest.TestCase):
    """Тесты разбора файла тестового репозитория."""

    def test_simple_parse(self):
        """Разбор простого файла."""
        data = parse_test_repo_file(
            "tests/test_repo_data/simple.txt")
        self.assertEqual(data, {"A": ["B"], "B": ["C"]})

    def test_diamond_parse(self):
        """Разбор файла с алмазной зависимостью."""
        data = parse_test_repo_file(
            "tests/test_repo_data/diamond.txt")
        self.assertEqual(data, {"A": ["B", "C"], "B": ["D"],
                                "C": ["D"]})

    def test_cycle_parse(self):
        """Разбор файла с циклом."""
        data = parse_test_repo_file(
            "tests/test_repo_data/cycle.txt")
        self.assertEqual(data, {"A": ["B"], "B": ["C"], "C": ["A"]})


class TestMakeTestFetchFn(unittest.TestCase):
    """Тесты функции создания fetch для тестового репозитория."""

    def test_fetch_existing(self):
        """Получение зависимостей существующего пакета."""
        graph_data = {"A": ["B", "C"]}
        fetch_fn = make_test_fetch_fn(graph_data)
        self.assertEqual(fetch_fn("A"), ["B", "C"])

    def test_fetch_missing(self):
        """Получение зависимостей неизвестного пакета."""
        graph_data = {"A": ["B"]}
        fetch_fn = make_test_fetch_fn(graph_data)
        self.assertEqual(fetch_fn("Z"), [])


if __name__ == "__main__":
    unittest.main()
