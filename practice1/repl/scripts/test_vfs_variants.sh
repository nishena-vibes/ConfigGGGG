#!/usr/bin/env bash
# 1. Минимальная VFS
python3 src/main.py --vfs tests/vfs_minimal.csv --script tests/startup_test.txt

# 2. VFS с несколькими файлами
python3 src/main.py --vfs tests/vfs_multi.csv --script tests/startup_test.txt

# 3. VFS с 3+ уровнями вложенности
python3 src/main.py --vfs tests/vfs_deep.csv --script tests/startup_test.txt
