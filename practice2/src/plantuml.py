"""Генерация PlantUML диаграммы графа зависимостей (этап 5)."""


def generate_plantuml(graph):
    """Генерировать текст PlantUML для графа зависимостей."""
    lines = ["@startuml", ""]
    for package in sorted(graph.all_packages()):
        for dep in sorted(graph.neighbors(package)):
            lines.append(f'"{package}" --> "{dep}"')
    lines.append("")
    lines.append("@enduml")
    return "\n".join(lines)


def generate_ascii_tree(graph, start):
    """Генерировать ASCII-дерево зависимостей, укоренённое в start."""
    lines = [start]
    _build_ascii_tree(graph, start, lines, "", set())
    return "\n".join(lines)


def _build_ascii_tree(graph, package, lines, prefix, visited):
    """Рекурсивно построить ветви ASCII-дерева.

    visited предотвращает бесконечную рекурсию на циклах, но edge
    всё равно печатается, чтобы показать связь.
    """
    if package in visited:
        return
    visited.add(package)
    deps = sorted(graph.neighbors(package))
    for i, dep in enumerate(deps):
        is_last = i == len(deps) - 1
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{dep}")
        if dep not in visited:
            extension = "    " if is_last else "│   "
            _build_ascii_tree(graph, dep, lines, prefix + extension,
                              visited)
