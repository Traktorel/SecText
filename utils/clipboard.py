from __future__ import annotations


def copy_to_clipboard(widget, text: str) -> None:
    widget.clipboard_clear()
    widget.clipboard_append(text)
    widget.update()
