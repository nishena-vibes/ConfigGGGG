"""Тесты извлечения зависимостей Maven (этап 2)."""

import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, "src")

from repo import extract_dependencies, fetch_dependencies, parse_package

METADATA_XML = b"""<?xml version="1.0"?>
<metadata xmlns="http://maven.apache.org/POM/4.0.0">
  <groupId>org.example</groupId>
  <artifactId>lib</artifactId>
  <versioning>
    <latest>1.2</latest>
    <versions>
      <version>1.0</version>
      <version>1.2</version>
    </versions>
  </versioning>
</metadata>
"""

POM_XML = b"""<?xml version="1.0"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.example</groupId>
  <artifactId>lib</artifactId>
  <version>1.2</version>
  <dependencies>
    <dependency>
      <groupId>org.example</groupId>
      <artifactId>dep-a</artifactId>
      <version>2.0</version>
    </dependency>
    <dependency>
      <groupId>com.other</groupId>
      <artifactId>dep-b</artifactId>
    </dependency>
  </dependencies>
</project>
"""


class _FakeResponse:
    def __init__(self, data):
        self._data = data

    def read(self):
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class TestRepo(unittest.TestCase):
    """Тесты модуля repo."""

    @patch("repo.urlopen")
    def test_fetch_dependencies_with_version(self, mock_urlopen):
        """Явно заданная версия загружает соответствующий POM."""
        mock_urlopen.return_value = _FakeResponse(POM_XML)
        deps = fetch_dependencies(
            "https://repo.example.com/maven2", "org.example:lib:1.2"
        )
        self.assertIn("org.example:dep-a:2.0", deps)
        self.assertIn("com.other:dep-b", deps)

    @patch("repo.urlopen")
    def test_resolve_latest_version(self, mock_urlopen):
        """Без версии используется latest из maven-metadata.xml."""

        def side_effect(url, timeout=10):
            if "maven-metadata" in url:
                return _FakeResponse(METADATA_XML)
            return _FakeResponse(POM_XML)

        mock_urlopen.side_effect = side_effect
        deps = fetch_dependencies(
            "https://repo.example.com/maven2", "org.example:lib"
        )
        self.assertIn("org.example:dep-a:2.0", deps)

    def test_parse_package(self):
        """Разбор полных координат пакета."""
        group, art, ver = parse_package("org.example:lib:1.2")
        self.assertEqual((group, art, ver), ("org.example", "lib", "1.2"))

    def test_parse_package_no_version(self):
        """Разбор пакета без версии."""
        group, art, ver = parse_package("org.example:lib")
        self.assertEqual((group, art, ver), ("org.example", "lib", None))

    def test_parse_package_bad_format(self):
        """Неверный формат пакета завершает программу."""
        with self.assertRaises(SystemExit):
            parse_package("badformat")

    def test_extract_dependencies_no_deps(self):
        """POM без зависимостей возвращает пустой список."""
        pom = b"<project xmlns='http://maven.apache.org/POM/4.0.0'></project>"
        self.assertEqual(extract_dependencies(pom), [])


if __name__ == "__main__":
    unittest.main()
