from __future__ import annotations

import customtkinter as ctk

from .base import TabBase


class SubstitutionTab(TabBase):
    def __init__(self, master, status_callback, crypto_manager, background_color: str = "#171717", surface_color: str = "#242424") -> None:
        self.crypto_manager = crypto_manager
        self.selected_cipher = ctk.StringVar(value="ROT13")
        self.vigenere_mode = ctk.StringVar(value="Encrypt")
        self.shift_value = ctk.StringVar(value="3")
        self.keyword_value = ctk.StringVar(value="")
        self.cipher_selector = None
        self.cipher_title_label = None
        self.cipher_subtitle_label = None
        self.output_title_label = None
        self.output_subtitle_label = None
        self.shift_frame = None
        self.shift_entry = None
        self.keyword_frame = None
        self.keyword_entry = None
        self.vigenere_mode_frame = None
        self.vigenere_mode_selector = None
        self.action_button = None
        super().__init__(master, status_callback, background_color, surface_color)
        self._build_ui()

    def _build_ui(self) -> None:
        intro_card = self.make_card(
            "Substitution ciphers",
            "Pick a cipher from the list, enter text, and the page will update its instructions for that specific cipher.",
        )
        intro_card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        intro_card.grid_columnconfigure(0, weight=1)

        selector_card = self.make_card(
            "Cipher list",
            "Each cipher is shown on its own line so it is easy to pick one and see the page update immediately.",
        )
        selector_card.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        selector_card.grid_columnconfigure(0, weight=1)

        selector_label = ctk.CTkLabel(selector_card, text="Available ciphers")
        selector_label.grid(row=2, column=0, sticky="w", padx=18, pady=(14, 6))

        cipher_list_frame = ctk.CTkFrame(selector_card, fg_color="transparent")
        cipher_list_frame.grid(row=3, column=0, sticky="ew", padx=18, pady=(0, 18))
        cipher_list_frame.grid_columnconfigure(0, weight=1)

        for row_index, cipher_name in enumerate(self._cipher_configs().keys()):
            cipher_button = ctk.CTkRadioButton(
                cipher_list_frame,
                text=cipher_name,
                variable=self.selected_cipher,
                value=cipher_name,
                command=lambda name=cipher_name: self._select_cipher(name),
            )
            cipher_button.grid(row=row_index, column=0, sticky="w", pady=(0, 10))

        cipher_card = ctk.CTkFrame(self, corner_radius=18, fg_color=self.surface_color)
        cipher_card.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        cipher_card.grid_columnconfigure(0, weight=1)
        self.cards.append(cipher_card)

        self.cipher_title_label = ctk.CTkLabel(cipher_card, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.cipher_title_label.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))

        self.cipher_subtitle_label = ctk.CTkLabel(cipher_card, text="", text_color=("gray35", "gray75"), justify="left")
        self.cipher_subtitle_label.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        text_label = ctk.CTkLabel(cipher_card, text="Text to encrypt or decrypt")
        text_label.grid(row=2, column=0, sticky="w", padx=18, pady=(0, 6))

        self.input_box = ctk.CTkTextbox(cipher_card, height=160, wrap="word")
        self.input_box.grid(row=3, column=0, sticky="ew", padx=18)

        self.shift_frame = ctk.CTkFrame(cipher_card, fg_color="transparent")
        self.shift_frame.grid(row=4, column=0, sticky="ew", padx=18, pady=(14, 0))
        self.shift_frame.grid_columnconfigure(1, weight=1)

        shift_label = ctk.CTkLabel(self.shift_frame, text="Shift amount")
        shift_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        self.shift_entry = ctk.CTkEntry(self.shift_frame, textvariable=self.shift_value, width=120)
        self.shift_entry.grid(row=0, column=1, sticky="w")

        self.keyword_frame = ctk.CTkFrame(cipher_card, fg_color="transparent")
        self.keyword_frame.grid(row=5, column=0, sticky="ew", padx=18, pady=(14, 0))
        self.keyword_frame.grid_columnconfigure(1, weight=1)

        keyword_label = ctk.CTkLabel(self.keyword_frame, text="Keyword")
        keyword_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        self.keyword_entry = ctk.CTkEntry(self.keyword_frame, textvariable=self.keyword_value, width=200, placeholder_text="Enter a keyword")
        self.keyword_entry.grid(row=0, column=1, sticky="w")

        self.vigenere_mode_frame = ctk.CTkFrame(cipher_card, fg_color="transparent")
        self.vigenere_mode_frame.grid(row=6, column=0, sticky="ew", padx=18, pady=(14, 0))
        self.vigenere_mode_frame.grid_columnconfigure(1, weight=1)

        mode_label = ctk.CTkLabel(self.vigenere_mode_frame, text="Vigenere mode")
        mode_label.grid(row=0, column=0, sticky="w", padx=(0, 12))

        self.vigenere_mode_selector = ctk.CTkSegmentedButton(
            self.vigenere_mode_frame,
            values=["Encrypt", "Decrypt"],
            command=self._select_vigenere_mode,
        )
        self.vigenere_mode_selector.set(self.vigenere_mode.get())
        self.vigenere_mode_selector.grid(row=0, column=1, sticky="w")

        button_row = ctk.CTkFrame(cipher_card, fg_color="transparent")
        button_row.grid(row=7, column=0, sticky="ew", padx=18, pady=18)
        button_row.grid_columnconfigure((0, 1), weight=1)

        self.action_button = ctk.CTkButton(button_row, text="", command=self.apply_cipher)
        self.action_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        clear_button = ctk.CTkButton(button_row, text="Clear", command=self.clear_fields)
        clear_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        output_card = ctk.CTkFrame(self, corner_radius=18, fg_color=self.surface_color)
        output_card.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        output_card.grid_columnconfigure(0, weight=1)
        self.cards.append(output_card)

        self.output_title_label = ctk.CTkLabel(output_card, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.output_title_label.grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))

        self.output_subtitle_label = ctk.CTkLabel(output_card, text="", text_color=("gray35", "gray75"), justify="left")
        self.output_subtitle_label.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        self.output_box = self.create_output_box(output_card, height=120)
        self.output_box.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        self.set_output_text(self.output_box, "")

        self._update_cipher_page(self.selected_cipher.get())

    def _cipher_configs(self) -> dict[str, dict[str, str]]:
        return {

            "Atbash": {
                "title": "Atbash",
                "description": "A mirrored alphabet substitution where A becomes Z, B becomes Y, and so on.",
                "button": "Apply Atbash",
                "output": "The result of applying the Atbash substitution to the input text.",
                "status": "Atbash applied successfully.",
                "uses_shift": False,
                "uses_keyword": False,
            },
            "Caesar Shift": {
                "title": "Caesar Shift",
                "description": "A classic shift cipher that moves each letter forward or backward by the chosen number of places.",
                "button": "Apply Caesar Shift",
                "output": "The result of applying the Caesar shift to the input text.",
                "status": "Caesar shift applied successfully.",
                "uses_shift": True,
                "uses_keyword": False,
            },
                "ROT13": {
                "title": "ROT13",
                "description": "A simple letter shift that moves each alphabetic character by 13 places. Applying it twice returns the original text.",
                "button": "Apply ROT13",
                "output": "The result of applying ROT13 to the input text.",
                "status": "ROT13 applied successfully.",
                "uses_shift": False,
                "uses_keyword": False,
            },
            "ROT47": {
                "title": "ROT47",
                "description": "A letter and symbol shift that moves each character in the ROT47 range by 47 places. Applying it twice returns the original text.",
                "button": "Apply ROT47",
                "output": "The result of applying ROT47 to the input text.",
                "status": "ROT47 applied successfully.",
                "uses_shift": False,
                "uses_keyword": False,
            },
            "Vigenere Cipher": {
                "title": "Vigenere Cipher",
                "description": "A method of encrypting text by applying a series of Caesar shifts based on the letters of a keyword.",
                "button": "Apply Vigenere Cipher",
                "output": "The result of applying the Vigenere cipher to the input text.",
                "status_encrypt": "Vigenere cipher encrypted successfully.",
                "status_decrypt": "Vigenere cipher decrypted successfully.",
                "uses_shift": False,
                "uses_keyword": True,
                "uses_vigenere_mode": True,
            },
        }

    def _select_cipher(self, cipher_name: str) -> None:
        self.selected_cipher.set(cipher_name)
        self._update_cipher_page(cipher_name)

    def _select_vigenere_mode(self, mode: str) -> None:
        self.vigenere_mode.set(mode)

        if self.selected_cipher.get() == "Vigenere Cipher":
            self._update_cipher_page("Vigenere Cipher")

    def _update_cipher_page(self, cipher_name: str) -> None:
        config = self._cipher_configs().get(cipher_name, self._cipher_configs()["ROT13"])

        self.cipher_title_label.configure(text=config["title"])
        self.cipher_subtitle_label.configure(text=config["description"])
        self.action_button.configure(text=self._action_button_text(cipher_name, config))
        self.output_title_label.configure(text=self._output_title(cipher_name, config))
        self.output_subtitle_label.configure(text=self._output_subtitle(cipher_name, config))

        if config.get("uses_shift"):
            self.shift_frame.grid()
        else:
            self.shift_frame.grid_remove()

        if config.get("uses_keyword"):
            self.keyword_frame.grid()
        else:
            self.keyword_frame.grid_remove()

        if config.get("uses_vigenere_mode"):
            self.vigenere_mode_frame.grid()
        else:
            self.vigenere_mode_frame.grid_remove()

        self.set_output_text(self.output_box, "")

    def _action_button_text(self, cipher_name: str, config: dict[str, str]) -> str:
        if cipher_name != "Vigenere Cipher":
            return config["button"]

        mode = self.vigenere_mode.get()
        return f"{mode} Vigenere Cipher"

    def _output_title(self, cipher_name: str, config: dict[str, str]) -> str:
        if cipher_name != "Vigenere Cipher":
            return f"{config['title']} output"

        return f"Vigenere {self.vigenere_mode.get()} output"

    def _output_subtitle(self, cipher_name: str, config: dict[str, str]) -> str:
        if cipher_name != "Vigenere Cipher":
            return config["output"]

        if self.vigenere_mode.get() == "Decrypt":
            return "The result of decrypting the input text with the Vigenere cipher."

        return "The result of encrypting the input text with the Vigenere cipher."

    def apply_cipher(self) -> None:
        input_text = self.read_textbox(self.input_box)
        if not input_text:
            self.set_status("Please enter some text first.")
            return

        cipher_name = self.selected_cipher.get()

        try:
            if cipher_name == "ROT13":
                result = self._apply_rot13(input_text)
            elif cipher_name == "Atbash":
                result = self._apply_atbash(input_text)
            elif cipher_name == "Caesar Shift":
                result = self._apply_caesar_shift(input_text)
            elif cipher_name == "ROT47":
                result = self._apply_rot47(input_text)
            elif cipher_name == "Vigenere Cipher":
                keyword = self.keyword_value.get().strip()
                if self.vigenere_mode.get() == "Decrypt":
                    result = self._apply_vigenere_decrypt(input_text, keyword)
                else:
                    result = self._apply_vigenere_encrypt(input_text, keyword)
            else:
                raise ValueError("Select a supported cipher.")
        except ValueError as exc:
            self.set_status(str(exc))
            return

        self.set_output_text(self.output_box, result)
        if cipher_name == "Vigenere Cipher":
            if self.vigenere_mode.get() == "Decrypt":
                self.set_status(self._cipher_configs()[cipher_name]["status_decrypt"])
            else:
                self.set_status(self._cipher_configs()[cipher_name]["status_encrypt"])
            return

        self.set_status(self._cipher_configs()[cipher_name]["status"])

    def clear_fields(self) -> None:
        self.input_box.delete("1.0", "end")
        self.shift_value.set("3")
        self.keyword_value.set("")
        self.vigenere_mode.set("Encrypt")
        if self.vigenere_mode_selector is not None:
            self.vigenere_mode_selector.set("Encrypt")
        self.set_output_text(self.output_box, "")
        self.set_status("Fields cleared.")

    def _apply_rot13(self, text: str) -> str:
        return self._apply_caesar_shift_text(text, 13)

    def _apply_atbash(self, text: str) -> str:
        return "".join(self._atbash_char(character) for character in text)

    def _apply_rot47(self, text: str) -> str:
        result = []
        for character in text:
            ascii_code = ord(character)
            if 33 <= ascii_code <= 126:
                shifted_code = 33 + ((ascii_code - 33 + 47) % 94)
                result.append(chr(shifted_code))
            else:
                result.append(character)

        return "".join(result)

    def _apply_vigenere_encrypt(self, text: str, keyword: str) -> str:
        if not keyword.isalpha():
            raise ValueError("Keyword must consist of letters only.")

        result = []
        keyword_length = len(keyword)
        keyword_index = 0

        for character in text:
            if character.isalpha():
                shift = ord(keyword[keyword_index % keyword_length].lower()) - ord("a")
                shifted_char = self._shift_character(character, shift)
                result.append(shifted_char)
                keyword_index += 1
            else:
                result.append(character)

        return "".join(result)

    def _apply_vigenere_decrypt(self, text: str, keyword: str) -> str:
        if not keyword.isalpha():
            raise ValueError("Keyword must consist of letters only.")

        result = []
        keyword_length = len(keyword)
        keyword_index = 0

        for character in text:
            if character.isalpha():
                shift = ord(keyword[keyword_index % keyword_length].lower()) - ord("a")
                shifted_char = self._shift_character(character, -shift)
                result.append(shifted_char)
                keyword_index += 1
            else:
                result.append(character)

        return "".join(result)

    def _apply_caesar_shift(self, text: str) -> str:
        shift_value = self.shift_value.get().strip()
        if not shift_value:
            shift = 3
        else:
            try:
                shift = int(shift_value)
            except ValueError as exc:
                raise ValueError("Enter a whole number shift for Caesar Shift.") from exc

        return self._apply_caesar_shift_text(text, shift)

    def _apply_vigenere(self, text: str, keyword: str) -> str:
        if not keyword.isalpha():
            raise ValueError("Keyword must consist of letters only.")

        result = []
        keyword_length = len(keyword)
        keyword_index = 0

        for character in text:
            if character.isalpha():
                shift = ord(keyword[keyword_index % keyword_length].lower()) - ord("a")
                result.append(self._shift_character(character, shift))
                keyword_index += 1
            else:
                result.append(character)

        return "".join(result)

    @staticmethod
    def _apply_caesar_shift_text(text: str, shift: int) -> str:
        return "".join(SubstitutionTab._shift_character(character, shift) for character in text)

    @staticmethod
    def _shift_character(character: str, shift: int) -> str:
        if "a" <= character <= "z":
            base = ord("a")
            return chr(base + ((ord(character) - base + shift) % 26))

        if "A" <= character <= "Z":
            base = ord("A")
            return chr(base + ((ord(character) - base + shift) % 26))

        return character

    @staticmethod
    def _atbash_char(character: str) -> str:
        if "a" <= character <= "z":
            return chr(ord("z") - (ord(character) - ord("a")))

        if "A" <= character <= "Z":
            return chr(ord("Z") - (ord(character) - ord("A")))

        return character