"""Получение прямых зависимостей Maven-пакета из репозитория (этап 2)."""

import sys
import xml.etree.ElementTree as et
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

POM_NAMESPACE = {"m": "http://maven.apache.org/POM/4.0.0"}
REQUEST_TIMEOUT = 10
MIN_PACKAGE_PARTS = 2
MAX_PACKAGE_PARTS = 3


def parse_package(package):
    """Разбивает строку пакета на groupId, artifactId, version.

    Формат: groupId:artifactId[:version]
    """
    parts = package.split(":")
    if len(parts) < MIN_PACKAGE_PARTS or len(parts) > MAX_PACKAGE_PARTS:
        print(f"Error: неверный формат пакета: {package}")
        sys.exit(1)
    group_id = parts[0]
    artifact_id = parts[1]
    version = parts[2] if len(parts) == MAX_PACKAGE_PARTS else None
    return group_id, artifact_id, version


def build_pom_url(repo_url, group_id, artifact_id, version):
    """Формирует URL POM-файла пакета."""
    group_path = group_id.replace(".", "/")
    return (
        f"{repo_url.rstrip('/')}/{group_path}/{artifact_id}/{version}/"
        f"{artifact_id}-{version}.pom"
    )


def resolve_latest_version(repo_url, group_id, artifact_id):
    """Возвращает последнюю версию из maven-metadata.xml."""
    group_path = group_id.replace(".", "/")
    metadata_url = (
        f"{repo_url.rstrip('/')}/{group_path}/{artifact_id}/"
        f"maven-metadata.xml"
    )
    try:
        with urlopen(metadata_url, timeout=REQUEST_TIMEOUT) as response:
            data = response.read()
    except (URLError, HTTPError) as error:
        print(f"Error: не удалось получить метаданные: {error}")
        sys.exit(1)
    root = et.fromstring(data)
    versioning = root.find("versioning")
    if versioning is None:
        versioning = root.find("m:versioning", POM_NAMESPACE)
    if versioning is None:
        print("Error: метаданные не содержат версии")
        sys.exit(1)
    latest = versioning.find("latest")
    if latest is None or not latest.text:
        latest = versioning.find("m:latest", POM_NAMESPACE)
    if latest is None or not latest.text:
        print("Error: не найдена последняя версия")
        sys.exit(1)
    return latest.text


def fetch_pom_text(url):
    """Загружает текст POM по URL."""
    try:
        with urlopen(url, timeout=REQUEST_TIMEOUT) as response:
            return response.read()
    except HTTPError as error:
        print(f"Error: HTTP {error.code} при загрузке {url}")
        sys.exit(1)
    except URLError as error:
        print(f"Error: не удалось загрузить {url}: {error}")
        sys.exit(1)


def extract_dependencies(pom_text):
    """Извлекает прямые зависимости из текста POM."""
    try:
        root = et.fromstring(pom_text)
    except et.ParseError as error:
        print(f"Error: некорректный XML POM: {error}")
        sys.exit(1)
    dependencies = []
    deps_elem = root.find("m:dependencies", POM_NAMESPACE)
    if deps_elem is None:
        return dependencies
    for dep in deps_elem.findall("m:dependency", POM_NAMESPACE):
        group_id = dep.findtext("m:groupId", namespaces=POM_NAMESPACE)
        artifact_id = dep.findtext("m:artifactId", namespaces=POM_NAMESPACE)
        version = dep.findtext("m:version", namespaces=POM_NAMESPACE)
        if group_id and artifact_id:
            coord = f"{group_id}:{artifact_id}"
            if version:
                coord += f":{version}"
            dependencies.append(coord)
    return dependencies


def fetch_dependencies(repo_url, package):
    """Возвращает список прямых зависимостей пакета."""
    group_id, artifact_id, version = parse_package(package)
    if version is None:
        version = resolve_latest_version(repo_url, group_id, artifact_id)
    pom_url = build_pom_url(repo_url, group_id, artifact_id, version)
    pom_text = fetch_pom_text(pom_url)
    return extract_dependencies(pom_text)
