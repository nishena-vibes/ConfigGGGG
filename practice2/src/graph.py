"""Построение и обход графа зависимостей (этап 3)."""


class DependencyGraph:
    """Граф зависимостей пакетов."""

    def __init__(self):
        self._edges = {}

    def add_edge(self, parent, child):
        """Добавить ребро зависимости parent -> child."""
        self._edges.setdefault(parent, set()).add(child)

    def neighbors(self, package):
        """Вернуть прямые зависимости пакета."""
        return self._edges.get(package, set())

    def all_packages(self):
        """Вернуть все пакеты графа."""
        result = set(self._edges.keys())
        for deps in self._edges.values():
            result.update(deps)
        return result


def bfs_build_graph(fetch_fn, start, max_depth, filter_substring=None):
    """Построить граф рекурсивным BFS.

    fetch_fn(package) -> список прямых зависимостей.
    """
    graph = DependencyGraph()
    visited = {start: 0}
    _bfs_level(fetch_fn, graph, [(start, 0)], visited, max_depth,
               filter_substring)
    return graph


def _bfs_level(fetch_fn, graph, current_level, visited, max_depth,
               filter_substring):
    """Обработать один уровень BFS и рекурсивно перейти к следующему."""
    if not current_level:
        return
    next_level = []
    for package, depth in current_level:
        if depth >= max_depth:
            continue
        try:
            deps = fetch_fn(package)
        except SystemExit:
            continue
        for dep in deps:
            dep_key = normalize_package(dep)
            if _is_filtered(dep_key, filter_substring):
                continue
            graph.add_edge(package, dep_key)
            if dep_key not in visited:
                visited[dep_key] = depth + 1
                next_level.append((dep_key, depth + 1))
    _bfs_level(fetch_fn, graph, next_level, visited, max_depth,
               filter_substring)


def normalize_package(dep):
    """Привести зависимость к ключу group:artifact."""
    parts = dep.split(":")
    if len(parts) >= 2:
        return f"{parts[0]}:{parts[1]}"
    return dep


def _is_filtered(package, filter_substring):
    """Проверить, подлежит ли пакет фильтрации."""
    return filter_substring is not None and filter_substring in package
