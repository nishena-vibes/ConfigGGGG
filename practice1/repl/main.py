"""GUI эмулятор командной строки UNIX-подобной ОС для Варианта №26."""
import getpass
import platform
import sys
import tkinter as tk
from tkinter import font
from typing import Tuple

EMPTY_COUNT = 0
MAX_CD_ARGS = 1
SUCCESS_EXIT_CODE = 0

class ShellEngine:
    """Ядро обработки и синтаксического разбора команд."""

    def __init__(self) -> None:
        """Инициализирует словарь обработчиков команд оболочки."""
        self._handlers = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
        }

    def parse(self, raw_line: str) -> Tuple[str, list[str]]:
        """Разбивает строку ввода на команду и список аргументов."""
        tokens = raw_line.strip().split()
        if len(tokens) == EMPTY_COUNT:
            return "", []
        return tokens[0], tokens[1:]

    def execute(self, cmd: str, args: list[str]) -> str:
        """Выполняет переданную команду либо возвращает ошибку."""
        if cmd in self._handlers:
            return self._handlers[cmd](args)
        return f"Ошибка: неизвестная команда '{cmd}'"

    def cmd_ls(self, args: list[str]) -> str:
        """Заглушка команды ls с отображением переданных аргументов."""
        if len(args) > EMPTY_COUNT:
            args_repr = " ".join(args)
        else:
            args_repr = "<без аргументов>"
        return f"ls: вызвана с аргументами: {args_repr}"

    def cmd_cd(self, args: list[str]) -> str:
        """Заглушка команды cd с проверкой количества аргументов."""
        if len(args) > MAX_CD_ARGS:
            return "cd: ошибка: неверные аргументы (слишком много)"
        if len(args) == MAX_CD_ARGS:
            args_repr = args[0]
        else:
            args_repr = "<домашний каталог>"
        return f"cd: вызвана с аргументом: {args_repr}"


class EmulatorApp:
    """Графический интерфейс эмулятора терминала."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует интерфейс и обработчики событий."""
        self.root = root
        self.engine = ShellEngine()
        self._setup_window()
        self._build_ui()
        self._bind_events()

    def _setup_window(self) -> None:
        """Формирует заголовок и начальные размеры окна."""
        user = getpass.getuser()
        host = platform.node()
        self.root.title(f"Эмулятор [{user}@{host}]")
        self.root.geometry("740x440")
        self.root.minsize(480, 280)
        # ВАЖНО: задаём тёмный фон всему окну
        self.root.configure(bg="#181818")

    def _build_ui(self) -> None:
        """Создает и размещает элементы графического интерфейса."""
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        ui_font = font.nametofont("Roboto")
        ui_font.configure(size=12)

        self.output_text = tk.Text(
            self.root,
            bg="#181818",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            font=ui_font,
            state=tk.DISABLED,
            wrap=tk.WORD,
            bd=0,
            padx=8,
            pady=8,
        )
        self.output_text.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=(10, 6)
        )

        # ИСПРАВЛЕНИЕ: tk.Frame вместо ttk.Frame с явным цветом фона
        input_frame = tk.Frame(self.root, bg="#181818")
        input_frame.grid(
            row=1, column=0, sticky="ew", padx=10, pady=(0, 10)
        )
        input_frame.grid_columnconfigure(1, weight=1)

        # ИСПРАВЛЕНИЕ: tk.Label вместо ttk.Label с явными цветами
        self.prompt_lbl = tk.Label(
            input_frame,
            text="$ ",
            font=ui_font,
            bg="#181818",
            fg="#e0e0e0",
        )
        self.prompt_lbl.grid(row=0, column=0, padx=(0, 6), sticky="w")

        # ИСПРАВЛЕНИЕ: tk.Entry вместо ttk.Entry с явными цветами
        self.entry = tk.Entry(
            input_frame,
            font=ui_font,
            bg="#2a2a2a",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            relief="solid",
            bd=1,
        )
        self.entry.grid(row=0, column=1, sticky="ew", ipady=4)

        # ИСПРАВЛЕНИЕ: tk.Button вместо ttk.Button с явными цветами
        self.btn = tk.Button(
            input_frame,
            text="Ввод",
            command=self._on_submit,
            bg="#4a4a4a",
            fg="#e0e0e0",
            activebackground="#5a5a5a",
            activeforeground="#ffffff",
            relief="raised",
            bd=1,
            padx=12,
            pady=4,
            font=ui_font,
        )
        self.btn.grid(row=0, column=2, padx=(8, 0), sticky="e")

    def _bind_events(self) -> None:
        """Привязывает события клавиатуры и фокусировку."""
        self.entry.bind("<Return>", lambda _: self._on_submit())
        self.root.after(100, self.entry.focus_set)

    def _print_line(self, line: str) -> None:
        """Выводит строку текста в терминальную область."""
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, line + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def _on_submit(self) -> None:
        """Обрабатывает ввод команды из текстового поля."""
        raw_val = self.entry.get()
        self.entry.delete(0, tk.END)
        cmd, args = self.engine.parse(raw_val)
        if not cmd:
            return
        self._print_line(f"$ {raw_val}")
        if cmd == "exit":
            self.root.destroy()
            sys.exit(SUCCESS_EXIT_CODE)
        res = self.engine.execute(cmd, args)
        self._print_line(res)


def main() -> None:
    """Точка входа запуска графической оболочки."""
    root = tk.Tk()
    EmulatorApp(root)
    root.mainloop()


# ИСПРАВЛЕНО: было "if name == "main":"
if __name__ == "__main__":
    main()
