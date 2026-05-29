from __future__ import annotations

import customtkinter as ctk

from .base import TabBase

class SubstitutionTab(TabBase):
    def __init__(self, master, status_callback, crypto_manager, background_color: str = "#171717", surface_color: str = "#242424") -> None:
        self.crypto_manager = crypto_manager
        super().__init__(master, status_callback, background_color, surface_color)
        self._build_ui()

    def _build_ui(self) -> None:
        card = self.make_card("Substitution ciphers", "Encrypt and decrypt text using simple letter substitutions. Not recommended for strong security, but fun to experiment with!")
        card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        card.grid_columnconfigure(0, weight=1)

        placeholder_label = ctk.CTkLabel(card, text="This tab is still a work in progress. Stay tuned for updates!", font=ctk.CTkFont(size=14), text_color=("gray35", "gray75"))
        placeholder_label.grid(row=2, column=0, sticky="w", padx=18, pady=(14, 6))