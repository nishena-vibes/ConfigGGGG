"""Разбор файла тестового репозитория (этап 3)."""

TEST_REPO_SEPARATOR = ":"


def parse_test_repo_file(path):
    """Разобрать файл тестового репозитория.

    Формат строки: A: B C  (A зависит от B и C).
    Пакеты называются большими латинскими буквами.
    """
    graph_data = {}
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if TEST_REPO_SEPARATOR not in line:
                continue
            parent, children_str = line.split(TEST_REPO_SEPARATOR, 1)
            parent = parent.strip()
            children = [c.strip() for c in children_str.split()
                        if c.strip()]
            graph_data[parent] = children
    return graph_data


def make_test_fetch_fn(graph_data):
    """Создать функцию получения зависимостей для тестового репозитория."""

    def fetch(package):
        return list(graph_data.get(package, []))

    return fetch
