from __future__ import annotations

import hashlib


class HashGenerator:
    @staticmethod
    def sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()
