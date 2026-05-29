from __future__ import annotations

import sys

import customtkinter as ctk


class TabBase(ctk.CTkScrollableFrame):
    def __init__(self, master, status_callback=None, background_color: str = "#171717", surface_color: str = "#242424") -> None:
        super().__init__(master, fg_color=background_color)
        self.status_callback = status_callback
        self.background_color = background_color
        self.surface_color = surface_color
        self.cards = []
        self.grid_columnconfigure(0, weight=1)
        self.pack(fill="both", expand=True, padx=18, pady=18)
        self.bind_all("<MouseWheel>", self._on_mouse_wheel, add="+")
        self.bind_all("<Button-4>", self._on_mouse_wheel, add="+")
        self.bind_all("<Button-5>", self._on_mouse_wheel, add="+")

    def set_status(self, message: str) -> None:
        if callable(self.status_callback):
            self.status_callback(message)

    def make_card(self, title: str, subtitle: str | None = None):
        card = ctk.CTkFrame(self, corner_radius=18, fg_color=self.surface_color)
        card.grid_columnconfigure(0, weight=1)
        self.cards.append(card)

        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))

        if subtitle:
            subtitle_label = ctk.CTkLabel(card, text=subtitle, text_color=("gray35", "gray75"), justify="left")
            subtitle_label.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        return card

    def apply_theme(self, background_color: str, surface_color: str) -> None:
        self.background_color = background_color
        self.surface_color = surface_color
        self.configure(fg_color=background_color)

        for card in self.cards:
            card.configure(fg_color=surface_color)

    def _widget_belongs_to_self(self, widget) -> bool:
        if widget == self:
            return True

        parent = getattr(widget, "master", None)
        if parent is None:
            return False

        return self._widget_belongs_to_self(parent)

    def _on_mouse_wheel(self, event) -> None:
        if not self._widget_belongs_to_self(event.widget):
            return

        if event.num == 4:
            delta = 1
        elif event.num == 5:
            delta = -1
        else:
            if sys.platform.startswith("win"):
                delta = int(event.delta / 120)
            else:
                delta = int(event.delta)

        if delta == 0:
            return

        if sys.platform.startswith("win"):
            units = -delta
        elif sys.platform == "darwin":
            units = -delta
        else:
            units = -delta

        self._parent_canvas.yview_scroll(units, "units")

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
