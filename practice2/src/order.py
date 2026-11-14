"""Порядок загрузки зависимостей (этап 4)."""


def topological_sort(graph, start):
    """Вернуть порядок загрузки зависимостей (сначала зависимости).

    Обход в глубину с пост-порядком: зависимость добавляется в результат
    перед пакетом, от которого она зависит. Циклы обрабатываются через
    множество посещённых пакетов.
    """
    visited = set()
    order = []

    def visit(package):
        if package in visited:
            return
        visited.add(package)
        for dep in sorted(graph.neighbors(package)):
            visit(dep)
        order.append(package)

    visit(start)
    return order


def load_order(graph, start):
    """Вернуть список пакетов в порядке загрузки."""
    return topological_sort(graph, start)
