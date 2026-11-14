"""Главный модуль GUI эмулятора оболочки ОС."""

import os
import socket
import tkinter as tk
from cli import parse_arguments
from commands import (
    cmd_cd,
    cmd_ls,
    cmd_rm,
    cmd_touch,
    cmd_uname,
    cmd_wc,
    resolve_path,
)
from script_runner import run_script_gui
from vfs import MemoryVFS

FIRST_ARG = 0
SECOND_ARG = 1


class ShellEmulator:
    """Главный класс эмулятора оболочки с графическим интерфейсом."""

    def __init__(self, root, vfs_manager, cli_args):
        """Инициализирует окно GUI, параметры и состояние оболочки."""
        self.root = root
        self.vfs = vfs_manager
        self.cli_args = cli_args
        self.running = True
        self.current_dir = "/"
        self._setup_window_title()
        self._setup_text_widget()
        self._print_debug_config()
        self.show_prompt()

    def _setup_window_title(self):
        """Формирует заголовок окна на основе данных реальной ОС."""
        try:
            user = os.getlogin()
        except OSError:
            user = os.environ.get("USER", "user")
        host = socket.gethostname()
        self.root.title(f"Эмулятор [{user}@{host}]")

    def _setup_text_widget(self):
        """Настраивает текстовый виджет терминала."""
        self.text = tk.Text(
            self.root,
            bg="black",
            fg="white",
            font=("Consolas", 12),
            insertbackground="white",
        )
        self.text.pack(expand=True, fill="both")
        self.text.bind("<Return>", self._on_enter)

    def _print_debug_config(self):
        """Выводит отладочную информацию о заданных параметрах."""
        vfs_val = self.cli_args.vfs or "default (in-memory)"
        scr_val = self.cli_args.script or "None"
        self.write_output(f"[DEBUG] VFS path: {vfs_val}\n")
        self.write_output(f"[DEBUG] Script path: {scr_val}\n")
        if self.vfs.load_error:
            self.write_output(f"{self.vfs.load_error}\n")

    def write_output(self, message):
        """Выводит текст в окно эмулятора."""
        self.text.insert(tk.END, message)
        self.text.see(tk.END)

    def show_prompt(self):
        """Выводит приглашение к вводу."""
        self.write_output(f"{self.current_dir}$ ")

    def _on_enter(self, _event):
        """Обрабатывает нажатие клавиши Enter пользователем."""
        line = self.text.get("insert linestart", "insert lineend")
        prompt = f"{self.current_dir}$ "
        cmd_str = (
            line[len(prompt):].strip()
            if line.startswith(prompt)
            else line.strip()
        )
        self.write_output("\n")
        self.execute_command(cmd_str)
        if self.running:
            self.show_prompt()
        return "break"

    def execute_command(self, command_str):
        """Выполняет команду и возвращает флаг наличия ошибки."""
        if not command_str:
            return False
        parts = command_str.split()
        cmd_name = parts[FIRST_ARG]
        args = parts[SECOND_ARG:]
        result = self._dispatch(cmd_name, args)
        if result:
            self.write_output(f"{result}\n")
        return bool(result and result.startswith("Error:"))

    def _dispatch(self, cmd_name, args):
        """Маршрутизирует вызов к нужной функции команды."""
        handlers = {
            "ls": self._handle_ls,
            "cd": self._handle_cd,
            "uname": cmd_uname,
            "wc": self._handle_wc,
            "touch": self._handle_touch,
            "rm": self._handle_rm,
            "exit": self._handle_exit,
        }
        handler = handlers.get(cmd_name)
        if handler is None:
            return f"Error: unknown command: {cmd_name}"
        return handler(args)

    def _handle_ls(self, args):
        """Обрабатывает команду ls."""
        target = (
            resolve_path(self.current_dir, args[FIRST_ARG])
            if args
            else self.current_dir
        )
        return cmd_ls(self.vfs, target)

    def _handle_cd(self, args):
        """Обрабатывает команду cd."""
        if not args:
            return "Error: cd: missing argument"
        res = cmd_cd(self.vfs, self.current_dir, args[FIRST_ARG])
        if not res.startswith("Error:"):
            self.current_dir = res
            return ""
        return res

    def _handle_wc(self, args):
        """Обрабатывает команду wc."""
        if not args:
            return "Error: wc: missing argument"
        path = resolve_path(self.current_dir, args[FIRST_ARG])
        return cmd_wc(self.vfs, path)

    def _handle_touch(self, args):
        """Обрабатывает команду touch."""
        if not args:
            return "Error: touch: missing argument"
        path = resolve_path(self.current_dir, args[FIRST_ARG])
        return cmd_touch(self.vfs, path)

    def _handle_rm(self, args):
        """Обрабатывает команду rm."""
        if not args:
            return "Error: rm: missing argument"
        path = resolve_path(self.current_dir, args[FIRST_ARG])
        return cmd_rm(self.vfs, path)

    def _handle_exit(self, _args):
        """Обрабатывает команду exit."""
        self.running = False
        self.root.quit()
        return "Exiting..."


def main():
    """Точка входа в приложение."""
    args = parse_arguments()
    vfs = MemoryVFS(args.vfs)
    root = tk.Tk()
    app = ShellEmulator(root, vfs, args)
    if args.script:
        run_script_gui(args.script, app)
    root.mainloop()


if __name__ == "__main__":
    main()
