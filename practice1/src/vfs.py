"""Модуль виртуальной файловой системы в памяти."""

import base64
import csv
import os


class MemoryVFS:
    """Виртуальная файловая система в памяти (источник: CSV)."""

    def __init__(self, vfs_path=None):
        """Загружает VFS из CSV или создает систему по умолчанию."""
        self.tree = {}
        self.load_error = None
        if vfs_path:
            self._load_from_csv(vfs_path)
        else:
            self._create_default()

    def _load_from_csv(self, path):
        """Читает CSV и заполняет дерево VFS в памяти."""
        try:
            with open(path, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self._parse_row(row)
        except Exception as exc:
            self.load_error = f"Error: failed to load VFS: {exc}"
            self._create_default()

    def _parse_row(self, row):
        """Обрабатывает одну строку CSV-файла."""
        clean = {
            (k.strip() if k else ""): (v.strip() if v else "")
            for k, v in row.items()
        }
        raw_path = clean.get("path", "")
        if not raw_path:
            return
        entry_type = clean.get("type", "file")
        b64_data = clean.get("content_b64", "")
        content = base64.b64decode(b64_data) if b64_data else b""
        self.tree[raw_path] = {"type": entry_type, "content": content}

    def _create_default(self):
        """Создает минимальную VFS по умолчанию в памяти."""
        self.tree = {
            "/": {"type": "dir", "content": b""},
            "/home": {"type": "dir", "content": b""},
            "/home/user": {"type": "dir", "content": b""},
            "/home/user/readme.txt": {
                "type": "file",
                "content": b"Hello World\nSecond line\n",
            },
        }
