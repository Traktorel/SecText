from __future__ import annotations

import random
import string


class PasswordGenerator:
    def __init__(self) -> None:
        self._random = random.SystemRandom()

    def generate(self, length: int) -> str:
        if length < 4:
            raise ValueError("Password length must be at least 4.")

        groups = [
            string.ascii_lowercase,
            string.ascii_uppercase,
            string.digits,
            string.punctuation,
        ]
        password_chars = [self._random.choice(group) for group in groups]
        pool = "".join(groups)
        password_chars.extend(self._random.choice(pool) for _ in range(length - len(password_chars)))
        self._random.shuffle(password_chars)
        return "".join(password_chars)
