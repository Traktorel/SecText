from __future__ import annotations

import base64
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

MAGIC_HEADER = b"SECTEXT1"
SALT_SIZE = 16
KDF_ITERATIONS = 390_000


class CryptoError(Exception):
    pass


class CryptoManager:
    def __init__(self, iterations: int = KDF_ITERATIONS) -> None:
        self.iterations = iterations

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        if not password:
            raise CryptoError("A password is required.")

        key_derivation = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.iterations,
        )
        return base64.urlsafe_b64encode(key_derivation.derive(password.encode("utf-8")))

    def _build_fernet(self, password: str, salt: bytes) -> Fernet:
        return Fernet(self._derive_key(password, salt))

    def encrypt_text(self, text: str, password: str) -> str:
        if not text.strip():
            raise CryptoError("Enter text before encrypting.")

        salt = os.urandom(SALT_SIZE)
        token = self._build_fernet(password, salt).encrypt(text.encode("utf-8"))
        salt_token = base64.urlsafe_b64encode(salt).decode("ascii")
        return f"SECTEXT1.{salt_token}.{token.decode('ascii')}"

    def decrypt_text(self, payload: str, password: str) -> str:
        if not payload.strip():
            raise CryptoError("Enter encrypted text first.")

        parts = payload.strip().split(".", 2)
        if len(parts) != 3 or parts[0] != "SECTEXT1":
            raise CryptoError("The encrypted text format is invalid.")

        try:
            salt = base64.urlsafe_b64decode(parts[1].encode("ascii"))
        except Exception as exc:
            raise CryptoError("The encrypted text contains an invalid salt.") from exc

        try:
            token = parts[2].encode("ascii")
            plaintext = self._build_fernet(password, salt).decrypt(token)
            return plaintext.decode("utf-8")
        except InvalidToken as exc:
            raise CryptoError("Wrong password or corrupted encrypted text.") from exc

    def encrypt_file(self, input_path: str, output_path: str, password: str) -> None:
        source = Path(input_path)
        target = Path(output_path)

        if not source.exists():
            raise CryptoError("The input file does not exist.")

        salt = os.urandom(SALT_SIZE)
        data = source.read_bytes()
        encrypted = self._build_fernet(password, salt).encrypt(data)
        target.write_bytes(MAGIC_HEADER + salt + encrypted)

    def decrypt_file(self, input_path: str, output_path: str, password: str) -> None:
        source = Path(input_path)
        target = Path(output_path)

        if not source.exists():
            raise CryptoError("The encrypted file does not exist.")

        data = source.read_bytes()
        if len(data) <= len(MAGIC_HEADER) + SALT_SIZE:
            raise CryptoError("The encrypted file is too short to be valid.")

        if not data.startswith(MAGIC_HEADER):
            raise CryptoError("This file was not created by SecText.")

        salt_start = len(MAGIC_HEADER)
        salt_end = salt_start + SALT_SIZE
        salt = data[salt_start:salt_end]
        token = data[salt_end:]

        try:
            decrypted = self._build_fernet(password, salt).decrypt(token)
            target.write_bytes(decrypted)
        except InvalidToken as exc:
            raise CryptoError("Wrong password or corrupted file.") from exc
