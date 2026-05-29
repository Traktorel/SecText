from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from utils import choose_input_file, choose_output_file, copy_to_clipboard
from .base import TabBase


class DecryptTab(TabBase):
    def __init__(self, master, status_callback, crypto_manager) -> None:
        self.crypto_manager = crypto_manager
        self.input_file_path = ""
        self.output_file_path = ""
        super().__init__(master, status_callback)
        self._build_ui()

    def _build_ui(self) -> None:
        overview = self.make_card(
            "Decrypt text and files",
            "Use the same password that was used when the content was encrypted.",
        )
        overview.grid(row=0, column=0, sticky="ew", pady=(0, 14))

        text_card = self.make_card("Text decryption", "Paste the encrypted string, then enter the matching password.")
        text_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        text_card.grid_columnconfigure(0, weight=1)

        text_label = ctk.CTkLabel(text_card, text="Encrypted text")
        text_label.grid(row=2, column=0, sticky="w", padx=18, pady=(0, 6))

        self.encrypted_text_box = ctk.CTkTextbox(text_card, height=160, wrap="word")
        self.encrypted_text_box.grid(row=3, column=0, sticky="ew", padx=18)

        password_label = ctk.CTkLabel(text_card, text="Password")
        password_label.grid(row=4, column=0, sticky="w", padx=18, pady=(14, 6))

        self.password_entry = ctk.CTkEntry(text_card, placeholder_text="Enter the decryption password", show="*")
        self.password_entry.grid(row=5, column=0, sticky="ew", padx=18)

        button_row = ctk.CTkFrame(text_card, fg_color="transparent")
        button_row.grid(row=6, column=0, sticky="ew", padx=18, pady=18)
        button_row.grid_columnconfigure((0, 1, 2), weight=1)

        decrypt_button = ctk.CTkButton(button_row, text="Decrypt Text", command=self.decrypt_text)
        decrypt_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        copy_button = ctk.CTkButton(button_row, text="Copy Result ⧉", command=self.copy_result)
        copy_button.grid(row=0, column=1, sticky="ew", padx=8)

        clear_button = ctk.CTkButton(button_row, text="Clear", command=self.clear_text_fields)
        clear_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        output_card = self.make_card("Decrypted output", "The decrypted text appears here after a successful unlock.")
        output_card.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        output_card.grid_columnconfigure(0, weight=1)

        self.decrypted_output = self.create_output_box(output_card, height=160)
        self.decrypted_output.grid(row=2, column=0, sticky="ew", padx=18)
        self.set_output_text(self.decrypted_output, "")

        file_card = self.make_card("File decryption", "Load a .sectext file and save the restored file to disk.")
        file_card.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        file_card.grid_columnconfigure(0, weight=1)
        file_card.grid_columnconfigure(1, weight=1)

        left_block = ctk.CTkFrame(file_card, fg_color="transparent")
        left_block.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        left_block.grid_columnconfigure(0, weight=1)

        right_block = ctk.CTkFrame(file_card, fg_color="transparent")
        right_block.grid(row=2, column=1, sticky="ew", padx=18, pady=(0, 18))
        right_block.grid_columnconfigure(0, weight=1)

        input_title = ctk.CTkLabel(left_block, text="Encrypted file")
        input_title.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.input_file_label = ctk.StringVar(value="No file selected")
        input_value = ctk.CTkLabel(left_block, textvariable=self.input_file_label, anchor="w", wraplength=400)
        input_value.grid(row=1, column=0, sticky="ew")

        choose_input_button = ctk.CTkButton(left_block, text="Choose File", command=self.choose_input_file)
        choose_input_button.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        output_title = ctk.CTkLabel(right_block, text="Output file")
        output_title.grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.output_file_label = ctk.StringVar(value="No output selected")
        output_value = ctk.CTkLabel(right_block, textvariable=self.output_file_label, anchor="w", wraplength=400)
        output_value.grid(row=1, column=0, sticky="ew")

        choose_output_button = ctk.CTkButton(right_block, text="Choose Save As", command=self.choose_output_file)
        choose_output_button.grid(row=2, column=0, sticky="ew", pady=(10, 0))

        file_button_row = ctk.CTkFrame(file_card, fg_color="transparent")
        file_button_row.grid(row=3, column=0, columnspan=2, sticky="ew", padx=18, pady=(0, 18))
        file_button_row.grid_columnconfigure(0, weight=1)

        decrypt_file_button = ctk.CTkButton(file_button_row, text="Decrypt File", command=self.decrypt_file)
        decrypt_file_button.grid(row=0, column=0, sticky="ew")

    def decrypt_text(self) -> None:
        try:
            result = self.crypto_manager.decrypt_text(self.read_textbox(self.encrypted_text_box), self.password_entry.get())
            self.set_output_text(self.decrypted_output, result)
            self.set_status("Text decrypted successfully.")
        except Exception as exc:
            self.set_status(str(exc))

    def copy_result(self) -> None:
        result = self.read_textbox(self.decrypted_output)
        if not result:
            self.set_status("Nothing to copy yet.")
            return

        copy_to_clipboard(self, result)
        self.set_status("Decrypted text copied to the clipboard.")

    def clear_text_fields(self) -> None:
        self.encrypted_text_box.delete("1.0", "end")
        self.password_entry.delete(0, "end")
        self.set_output_text(self.decrypted_output, "")
        self.set_status("Text fields cleared.")

    def choose_input_file(self) -> None:
        selected_path = choose_input_file("Select a file to decrypt")
        if not selected_path:
            return

        self.input_file_path = selected_path
        self.input_file_label.set(selected_path)

        if not self.output_file_path:
            self.output_file_path = self._suggest_output_path(selected_path)
            self.output_file_label.set(self.output_file_path)

        self.set_status("Encrypted file selected.")

    def choose_output_file(self) -> None:
        selected_path = choose_output_file(
            "Save decrypted file",
            "",
            (("All files", "*.*"),),
        )
        if not selected_path:
            return

        self.output_file_path = selected_path
        self.output_file_label.set(selected_path)
        self.set_status("Output file selected.")

    def decrypt_file(self) -> None:
        try:
            if not self.input_file_path:
                raise ValueError("Select an encrypted file first.")

            if not self.output_file_path:
                self.output_file_path = self._suggest_output_path(self.input_file_path)
                self.output_file_label.set(self.output_file_path)

            self.crypto_manager.decrypt_file(self.input_file_path, self.output_file_path, self.password_entry.get())
            self.set_status("File decrypted successfully.")
        except Exception as exc:
            self.set_status(str(exc))

    @staticmethod
    def _suggest_output_path(source_path: str) -> str:
        source = Path(source_path)
        if source.suffix == ".sectext":
            return str(source.with_suffix(""))
        return str(source.with_name(f"{source.stem}_decrypted"))
