import platform

ROOT_INDEX = 0
EXTRA_LINE = 1


def cmd_uname(args):
    """Выводит информацию о системе."""
    if args:
        return "Error: uname takes no arguments"
    return platform.system()


def cmd_ls(vfs, path):
    """Выводит список элементов указанной директории."""
    target = normalize_path(path)
    if target not in vfs.tree:
        return f"Error: directory not found: {path}"
    if vfs.tree[target]["type"] != "dir":
        return f"Error: not a directory: {path}"
    items = _collect_ls_items(vfs, target)
    return "  ".join(sorted(items))


def _collect_ls_items(vfs, target):
    """Собирает прямых потомков директории."""
    items = []
    prefix = target.rstrip("/") + "/"
    for full_path, info in vfs.tree.items():
        if full_path != target and full_path.startswith(prefix):
            remainder = full_path[len(prefix):]
            if "/" not in remainder:
                suffix = "/" if info["type"] == "dir" else ""
                items.append(remainder + suffix)
    return items


def cmd_cd(vfs, current_dir, new_dir):
    """Меняет текущую директорию с поддержкой '..' и '.'."""
    target = resolve_path(current_dir, new_dir)
    if target not in vfs.tree:
        return f"Error: not found: {new_dir}"
    if vfs.tree[target]["type"] != "dir":
        return f"Error: not a directory: {new_dir}"
    return target


def cmd_wc(vfs, path):
    """Считает строки, слова и байты в файле."""
    if path not in vfs.tree:
        return f"Error: file not found: {path}"
    if vfs.tree[path]["type"] != "file":
        return f"Error: not a file: {path}"
    content = vfs.tree[path]["content"]
    text = content.decode("utf-8", errors="ignore")
    lines = text.count("\n")
    if text and not text.endswith("\n"):
        lines += EXTRA_LINE
    words = len(text.split())
    return f"{lines} {words} {len(content)} {path}"


def cmd_touch(vfs, path):
    """Создает пустой файл в виртуальной памяти."""
    if path in vfs.tree:
        return f"Error: already exists: {path}"
    parent = get_parent(path)
    if parent not in vfs.tree:
        return f"Error: parent not found: {parent}"
    if vfs.tree[parent]["type"] != "dir":
        return f"Error: parent not a directory: {parent}"
    vfs.tree[path] = {"type": "file", "content": b""}
    return ""


def cmd_rm(vfs, path):
    """Удаляет файл из виртуальной памяти."""
    if path not in vfs.tree:
        return f"Error: not found: {path}"
    if vfs.tree[path]["type"] == "dir":
        return f"Error: is a directory: {path}"
    del vfs.tree[path]
    return ""


def resolve_path(current_dir, target_path):
    """Преобразует относительный или абсолютный путь в канонический."""
    if target_path.startswith("/"):
        raw = target_path
    elif current_dir == "/":
        raw = f"/{target_path}"
    else:
        raw = f"{current_dir}/{target_path}"
    return normalize_path(raw)


def normalize_path(path):
    """Нормализует путь, разрешая '.' и '..'."""
    stack = []
    for part in path.split("/"):
        if not part or part == ".":
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)


def get_parent(path):
    """Возвращает путь к родительской директории."""
    norm = normalize_path(path)
    idx = norm.rfind("/")
    if idx <= ROOT_INDEX:
        return "/"
    return norm[:idx]
