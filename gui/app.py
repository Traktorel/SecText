from __future__ import annotations

import tkinter as tk

import customtkinter as ctk

from crypto import CryptoManager, HashGenerator, PasswordGenerator
from gui.tabs import DecryptTab, EncryptTab, HashTab, PasswordTab, SubstitutionTab


class SecTextApp(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        super().__init__()

        self.title("SecureText")
        self.geometry("1040x900")
        self.minsize(920, 760)

        self.crypto_manager = CryptoManager()
        self.hash_generator = HashGenerator()
        self.password_generator = PasswordGenerator()
        self.status_var = ctk.StringVar(value="")
        self._background_canvas = None
        self._theme_transition_steps = 18
        self._theme_transition_index = 0
        self._theme_transition_target = "Dark"
        self._theme_transition_running = False
        self._theme_bg_color = self._background_color(ctk.get_appearance_mode())
        self._theme_surface_color = self._surface_color(ctk.get_appearance_mode())
        self.header_frame = None
        self.tab_frame = None
        self.tabview = None
        self.status_bar = None

        self._build_background()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_tabs()
        self._build_status_bar()
        self._update_theme_button()

    def _build_background(self) -> None:
        background_color = self._background_color(ctk.get_appearance_mode())
        self._background_canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=background_color)
        self._background_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.tk.call("lower", self._background_canvas._w)

    def _background_color(self, mode: str) -> str:
        return "#171717" if mode == "Dark" else "#F2F2F2"

    def _surface_color(self, mode: str) -> str:
        return "#232323" if mode == "Dark" else "#E6E6E6"

    def _build_header(self) -> None:
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self._theme_bg_color)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self.header_frame, text="SecureText", font=ctk.CTkFont(size=32, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=24, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            self.header_frame,
            text="Secure text encryption, file protection, hashes, and passwords in one scrollable workspace.",
            text_color=("gray35", "gray75"),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 18))

        self.theme_button = ctk.CTkButton(self.header_frame, command=self.toggle_theme, width=150)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=24, pady=18)

    def _build_tabs(self) -> None:
        self.tab_frame = ctk.CTkFrame(self, corner_radius=18, fg_color=self._theme_bg_color)
        self.tab_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 12))
        self.tab_frame.grid_columnconfigure(0, weight=1)
        self.tab_frame.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self.tab_frame, fg_color=self._theme_bg_color)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        encrypt_tab = self.tabview.add("Encrypt")
        decrypt_tab = self.tabview.add("Decrypt")
        hash_tab = self.tabview.add("Hash Generator")
        password_tab = self.tabview.add("Password Generator")
        substitution_tab = self.tabview.add("Substitution Ciphers")
        
        self.substitution_tab = SubstitutionTab(
            substitution_tab,
            self.set_status,
            self.crypto_manager,
            self._theme_bg_color,
            self._theme_surface_color,
        )
        self.encrypt_tab = EncryptTab(encrypt_tab, self.set_status, self.crypto_manager, self._theme_bg_color, self._theme_surface_color)
        self.decrypt_tab = DecryptTab(decrypt_tab, self.set_status, self.crypto_manager, self._theme_bg_color, self._theme_surface_color)
        self.hash_tab = HashTab(hash_tab, self.set_status, self.hash_generator, self._theme_bg_color, self._theme_surface_color)
        self.password_tab = PasswordTab(password_tab, self.set_status, self.password_generator, self._theme_bg_color, self._theme_surface_color)

    def _build_status_bar(self) -> None:
        self.status_bar = ctk.CTkFrame(self, corner_radius=0, fg_color=self._theme_bg_color)
        self.status_bar.grid(row=2, column=0, sticky="ew")
        self.status_bar.grid_columnconfigure(0, weight=1)

        status_label = ctk.CTkLabel(self.status_bar, textvariable=self.status_var, anchor="w")
        status_label.grid(row=0, column=0, sticky="ew", padx=24, pady=12)

    def _apply_theme_background(self) -> None:
        for widget in (self.header_frame, self.tab_frame, self.status_bar, self.tabview):
            if widget is not None:
                widget.configure(fg_color=self._theme_bg_color)

        for tab in (self.encrypt_tab, self.decrypt_tab, self.hash_tab, self.password_tab,self.substitution_tab):
            if tab is not None:
                tab.apply_theme(self._theme_bg_color, self._theme_surface_color)

        if self._background_canvas is not None:
            self._background_canvas.configure(bg=self._theme_bg_color)

    def _theme_colors(self, mode: str) -> tuple[str, str]:
        if mode == "Dark":
            return self._background_color("Dark"), self._background_color("Light")
        return self._background_color("Light"), self._background_color("Dark")

    def _start_theme_transition(self) -> None:
        if self._theme_transition_running:
            return

        self._theme_transition_running = True
        current_mode = ctk.get_appearance_mode()
        self._theme_transition_target = "Light" if current_mode == "Dark" else "Dark"
        start_color, target_color = self._theme_colors(current_mode)
        self._theme_bg_color = start_color
        self._theme_surface_color = self._surface_color(current_mode)

        if self._background_canvas is None:
            return

        self._background_canvas.configure(bg=start_color)
        self._background_canvas.start_color = start_color  # type: ignore[attr-defined]
        self._background_canvas.target_color = target_color  # type: ignore[attr-defined]
        self._background_canvas.update_idletasks()
        self._apply_theme_background()

        self.theme_button.configure(state="disabled")
        self._theme_transition_index = 0
        self._animate_theme_transition()

    def _animate_theme_transition(self) -> None:
        if self._background_canvas is None:
            return

        canvas = self._background_canvas
        width = max(self.winfo_width(), 1)
        height = max(self.winfo_height(), 1)
        center_x = width / 2
        center_y = height / 2
        max_radius = (width**2 + height**2) ** 0.5 / 2 + 12
        progress = self._theme_transition_index / max(self._theme_transition_steps, 1)
        radius = max_radius * progress

        canvas.delete("transition")
        canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill=canvas.target_color,  # type: ignore[attr-defined]
            outline=canvas.target_color,  # type: ignore[attr-defined]
            width=0,
            tags="transition",
        )

        if self._theme_transition_index == self._theme_transition_steps // 2:
            ctk.set_appearance_mode(self._theme_transition_target)
            self._update_theme_button()
            self._theme_bg_color = self._background_color(self._theme_transition_target)
            self._theme_surface_color = self._surface_color(self._theme_transition_target)
            self._apply_theme_background()

        if self._theme_transition_index >= self._theme_transition_steps:
            self._finish_theme_transition()
            return

        self._theme_transition_index += 1
        self.after(14, self._animate_theme_transition)

    def _finish_theme_transition(self) -> None:
        self._theme_transition_running = False
        self.theme_button.configure(state="normal")

    def _update_theme_button(self) -> None:
        current_mode = ctk.get_appearance_mode()
        button_text = "Switch to Light" if current_mode == "Dark" else "Switch to Dark"
        self.theme_button.configure(text=button_text)

    def set_status(self, message: str) -> None:
        self.status_var.set(message)

    def toggle_theme(self) -> None:
        self._start_theme_transition()

    def run(self) -> None:
        self.mainloop()
