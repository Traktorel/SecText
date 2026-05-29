from __future__ import annotations

import customtkinter as ctk

from utils import copy_to_clipboard
from .base import TabBase


class PasswordTab(TabBase):
    def __init__(self, master, status_callback, password_generator) -> None:
        self.password_generator = password_generator
        super().__init__(master, status_callback)
        self._build_ui()

    def _build_ui(self) -> None:
        overview = self.make_card(
            "Password generator",
            "Create a strong password with a customizable length.",
        )
        overview.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        generator_card = self.make_card("Generate password", "Use a length of at least 4 characters.")
        generator_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        generator_card.grid_columnconfigure(0, weight=1)

        length_label = ctk.CTkLabel(generator_card, text="Length")
        length_label.grid(row=2, column=0, sticky="w", padx=18, pady=(0, 6))

        self.length_entry = ctk.CTkEntry(generator_card, placeholder_text="16")
        self.length_entry.grid(row=3, column=0, sticky="ew", padx=18)
        self.length_entry.insert(0, "16")

        button_row = ctk.CTkFrame(generator_card, fg_color="transparent")
        button_row.grid(row=4, column=0, sticky="ew", padx=18, pady=18)
        button_row.grid_columnconfigure((0, 1), weight=1)

        generate_button = ctk.CTkButton(button_row, text="Generate Password", command=self.generate_password)
        generate_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        copy_button = ctk.CTkButton(button_row, text="Copy Password ⧉", command=self.copy_result)
        copy_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        output_card = self.make_card("Generated password", "The result appears below and can be copied to the clipboard.")
        output_card.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        output_card.grid_columnconfigure(0, weight=1)

        self.output_box = self.create_output_box(output_card, height=120)
        self.output_box.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        self.set_output_text(self.output_box, "")

    def generate_password(self) -> None:
        try:
            length = int(self.length_entry.get().strip())
            result = self.password_generator.generate(length)
            self.set_output_text(self.output_box, result)
            self.set_status("Password generated successfully.")
        except Exception as exc:
            self.set_status(str(exc))

    def copy_result(self) -> None:
        result = self.read_textbox(self.output_box)
        if not result:
            self.set_status("Nothing to copy yet.")
            return

        copy_to_clipboard(self, result)
        self.set_status("Password copied to the clipboard.")
