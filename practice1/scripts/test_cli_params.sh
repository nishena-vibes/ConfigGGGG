#!/usr/bin/env bash
# Запуск с VFS по умолчанию без скрипта
python3 src/main.py

# Запуск с пользовательской VFS
python3 src/main.py --vfs tests/vfs_multi.csv

# Запуск со стартовым скриптом и глубокой VFS
python3 src/main.py --vfs tests/vfs_deep.csv --script tests/startup_test.txt
