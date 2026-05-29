from __future__ import annotations

from tkinter import filedialog


def choose_input_file(title: str = "Select a file") -> str:
    return filedialog.askopenfilename(title=title)


def choose_output_file(title: str, default_extension: str, filetypes: tuple[tuple[str, str], ...]) -> str:
    return filedialog.asksaveasfilename(
        title=title,
        defaultextension=default_extension,
        filetypes=filetypes,
    )
