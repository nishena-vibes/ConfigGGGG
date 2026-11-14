"""Тесты порядка загрузки зависимостей (этап 4)."""

import sys
import unittest

sys.path.insert(0, "src")

from graph import DependencyGraph
from order import load_order


class TestLoadOrder(unittest.TestCase):
    """Тесты функции load_order (топологическая сортировка)."""

    def test_linear_chain(self):
        """Цепочка A -> B -> C: порядок C, B, A."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        order = load_order(graph, "A")
        self.assertEqual(order, ["C", "B", "A"])

    def test_diamond(self):
        """Алмаз: A->B,C; B->D; C->D. D загружается первым."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "D")
        order = load_order(graph, "A")
        self.assertEqual(order[0], "D")
        self.assertEqual(order[-1], "A")
        self.assertTrue(order.index("B") < order.index("A"))
        self.assertTrue(order.index("C") < order.index("A"))

    def test_cycle(self):
        """Цикл A->B->C->A: без зацикливания, все пакеты presentes."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        order = load_order(graph, "A")
        self.assertEqual(set(order), {"A", "B", "C"})
        self.assertEqual(len(order), 3)

    def test_no_dependencies(self):
        """Пакет без зависимостей: порядок содержит только его."""
        graph = DependencyGraph()
        order = load_order(graph, "A")
        self.assertEqual(order, ["A"])

    def test_dependencies_before_dependents(self):
        """Каждая зависимость предшествует зависимому пакету."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "E")
        order = load_order(graph, "A")
        for idx, package in enumerate(order):
            for dep in graph.neighbors(package):
                dep_idx = order.index(dep)
                self.assertLess(dep_idx, idx,
                                f"Зависимость {dep} должна preced {package}")


if __name__ == "__main__":
    unittest.main()
