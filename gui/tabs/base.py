from __future__ import annotations

import customtkinter as ctk


class TabBase(ctk.CTkScrollableFrame):
    def __init__(self, master, status_callback=None) -> None:
        super().__init__(master, fg_color="transparent")
        self.status_callback = status_callback
        self.pack(fill="both", expand=True, padx=18, pady=18)
        self.grid_columnconfigure(0, weight=1)

    def set_status(self, message: str) -> None:
        if callable(self.status_callback):
            self.status_callback(message)

    def make_card(self, title: str, subtitle: str | None = None):
        card = ctk.CTkFrame(self, corner_radius=18)
        card.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=20, weight="bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))

        if subtitle:
            subtitle_label = ctk.CTkLabel(card, text=subtitle, text_color=("gray35", "gray75"), justify="left")
            subtitle_label.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        return card

    @staticmethod
    def create_output_box(parent, height: int = 120):
        output_box = ctk.CTkTextbox(parent, height=height, wrap="word")
        output_box.grid_columnconfigure(0, weight=1)
        return output_box

    @staticmethod
    def set_output_text(output_box, text: str) -> None:
        output_box.configure(state="normal")
        output_box.delete("1.0", "end")
        output_box.insert("1.0", text)
        output_box.configure(state="disabled")

    @staticmethod
    def read_textbox(textbox) -> str:
        return textbox.get("1.0", "end").strip()
