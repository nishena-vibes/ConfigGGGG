import argparse


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument(
        "--vfs",
        type=str,
        default=None,
        help="Path to VFS CSV file",
    )
    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Path to startup script",
    )
    return parser.parse_args()
