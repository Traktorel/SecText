from __future__ import annotations

import customtkinter as ctk

from .base import TabBase


class HashTab(TabBase):
    def __init__(self, master, status_callback, hash_generator, background_color: str = "#171717", surface_color: str = "#242424") -> None:
        self.hash_generator = hash_generator
        super().__init__(master, status_callback, background_color, surface_color)
        self._build_ui()

    def _build_ui(self) -> None:
        input_card = self.make_card("Input text", "Hashes are useful for checking integrity and verifying files.")
        input_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        input_card.grid_columnconfigure(0, weight=1)

        text_label = ctk.CTkLabel(input_card, text="Text to hash")
        text_label.grid(row=2, column=0, sticky="w", padx=18, pady=(14, 6))

        self.input_box = ctk.CTkTextbox(input_card, height=160, wrap="word")
        self.input_box.grid(row=3, column=0, sticky="ew", padx=18)

        button_row = ctk.CTkFrame(input_card, fg_color="transparent")
        button_row.grid(row=4, column=0, sticky="ew", padx=18, pady=18)
        button_row.grid_columnconfigure((0, 1, 2), weight=1)

        hash_button = ctk.CTkButton(button_row, text="Generate SHA256", command=self.generate_hash)
        hash_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        copy_button = ctk.CTkButton(button_row, text="Copy Hash ⧉", command=self.copy_result)
        copy_button.grid(row=0, column=1, sticky="ew", padx=8)

        clear_button = ctk.CTkButton(button_row, text="Clear", command=self.clear_fields)
        clear_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        output_card = self.make_card("SHA-256 output", "The hash is shown as a 64-character hexadecimal string.")
        output_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        output_card.grid_columnconfigure(0, weight=1)

        self.output_box = self.create_output_box(output_card, height=120)
        self.output_box.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        self.set_output_text(self.output_box, "")

    def generate_hash(self) -> None:
        try:
            text_value = self.read_textbox(self.input_box)
            result = self.hash_generator.sha256(text_value)
            self.set_output_text(self.output_box, result)
            self.set_status("SHA-256 hash generated.")
        except Exception as exc:
            self.set_status(str(exc))

    def copy_result(self) -> None:
        result = self.read_textbox(self.output_box)
        if not result:
            self.set_status("Nothing to copy yet.")
            return

        from utils import copy_to_clipboard

        copy_to_clipboard(self, result)
        self.set_status("Hash copied to the clipboard.")

    def clear_fields(self) -> None:
        self.input_box.delete("1.0", "end")
        self.set_output_text(self.output_box, "")
        self.set_status("Hash fields cleared.")
