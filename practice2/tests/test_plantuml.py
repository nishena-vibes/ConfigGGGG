"""Тесты визуализации PlantUML и ASCII-дерева (этап 5)."""

import sys
import unittest

sys.path.insert(0, "src")

from graph import DependencyGraph
from plantuml import generate_ascii_tree, generate_plantuml


class TestPlantUml(unittest.TestCase):
    """Тесты генерации PlantUML."""

    def test_generate_plantuml_structure(self):
        """PlantUML начинается с @startuml и заканчивается @enduml."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        output = generate_plantuml(graph)
        self.assertTrue(output.startswith("@startuml"))
        self.assertTrue(output.endswith("@enduml"))
        self.assertIn('"A" --> "B"', output)

    def test_generate_plantuml_no_edges(self):
        """Граф без рёбер производит валидную обёртку PlantUML."""
        graph = DependencyGraph()
        output = generate_plantuml(graph)
        self.assertTrue(output.startswith("@startuml"))
        self.assertTrue(output.endswith("@enduml"))


class TestAsciiTree(unittest.TestCase):
    """Тесты генерации ASCII-дерева."""

    def test_linear_chain(self):
        """Линейная цепочка A -> B -> C."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        output = generate_ascii_tree(graph, "A")
        lines = output.split("\n")
        self.assertEqual(lines[0], "A")
        self.assertIn("└── B", lines[1])
        self.assertIn("    └── C", lines[2])

    def test_diamond(self):
        """Алмазная зависимость показывает оба пути к D."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "D")
        graph.add_edge("C", "D")
        output = generate_ascii_tree(graph, "A")
        self.assertIn("├── B", output)
        self.assertIn("└── C", output)
        self.assertIn("└── D", output)

    def test_cycle_no_infinite_loop(self):
        """Цикл не вызывает бесконечной рекурсии."""
        graph = DependencyGraph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        output = generate_ascii_tree(graph, "A")
        self.assertIn("A", output)
        self.assertIn("B", output)
        self.assertIn("C", output)

    def test_no_dependencies(self):
        """Пакет без зависимостей — только его имя."""
        graph = DependencyGraph()
        output = generate_ascii_tree(graph, "A")
        self.assertEqual(output, "A")


if __name__ == "__main__":
    unittest.main()
