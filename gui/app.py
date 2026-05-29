from __future__ import annotations

import customtkinter as ctk

from crypto import CryptoManager, HashGenerator, PasswordGenerator
from gui.tabs import DecryptTab, EncryptTab, HashTab, PasswordTab


class SecTextApp(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        super().__init__()

        self.title("SecText | SecureText")
        self.geometry("1180x860")
        self.minsize(980, 720)

        self.crypto_manager = CryptoManager()
        self.hash_generator = HashGenerator()
        self.password_generator = PasswordGenerator()
        self.status_var = ctk.StringVar(value="Ready. Pick a tab to begin.")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_tabs()
        self._build_status_bar()
        self._update_theme_button()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header, text="SecText", font=ctk.CTkFont(size=32, weight="bold"))
        title.grid(row=0, column=0, sticky="w", padx=24, pady=(18, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Secure text encryption, file protection, hashes, and passwords in one focused workspace.",
            text_color=("gray35", "gray75"),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=24, pady=(0, 18))

        self.theme_button = ctk.CTkButton(header, command=self.toggle_theme, width=150)
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=24, pady=18)

    def _build_tabs(self) -> None:
        tab_frame = ctk.CTkFrame(self, corner_radius=18)
        tab_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 12))
        tab_frame.grid_columnconfigure(0, weight=1)
        tab_frame.grid_rowconfigure(0, weight=1)

        tabview = ctk.CTkTabview(tab_frame)
        tabview.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        encrypt_tab = tabview.add("Encrypt")
        decrypt_tab = tabview.add("Decrypt")
        hash_tab = tabview.add("Hash Generator")
        password_tab = tabview.add("Password Generator")

        EncryptTab(encrypt_tab, self.set_status, self.crypto_manager)
        DecryptTab(decrypt_tab, self.set_status, self.crypto_manager)
        HashTab(hash_tab, self.set_status, self.hash_generator)
        PasswordTab(password_tab, self.set_status, self.password_generator)

    def _build_status_bar(self) -> None:
        status_bar = ctk.CTkFrame(self, corner_radius=0)
        status_bar.grid(row=2, column=0, sticky="ew")
        status_bar.grid_columnconfigure(0, weight=1)

        status_label = ctk.CTkLabel(status_bar, textvariable=self.status_var, anchor="w")
        status_label.grid(row=0, column=0, sticky="ew", padx=24, pady=12)

    def _update_theme_button(self) -> None:
        current_mode = ctk.get_appearance_mode()
        button_text = "Change Theme" if current_mode == "Dark" else "Change Theme"
        self.theme_button.configure(text=button_text)

    def set_status(self, message: str) -> None:
        self.status_var.set(message)

    def toggle_theme(self) -> None:
        next_mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(next_mode)
        self._update_theme_button()
        self.set_status(f"{next_mode} theme enabled.")

    def run(self) -> None:
        self.mainloop()
