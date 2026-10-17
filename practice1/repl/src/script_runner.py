"""Модуль выполнения стартового скрипта в GUI."""

import os


def run_script_gui(script_path, app):
    """Выполняет стартовый скрипт и останавливается при первой ошибке."""
    if not os.path.exists(script_path):
        app.write_output(f"Error: script not found: {script_path}\n")
        return
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            _process_lines(file, app)
    except OSError as exc:
        app.write_output(f"Error: cannot read script: {exc}\n")


def _process_lines(file, app):
    """Построчно выполняет команды скрипта до первой ошибки."""
    for line in file:
        cmd = line.strip()
        if not cmd:
            continue
        app.write_output(f"{cmd}\n")
        has_error = app.execute_command(cmd)
        if not app.running:
            break
        app.show_prompt()
        if has_error:
            app.write_output("Script execution stopped due to error.\n")
            app.show_prompt()
            break
