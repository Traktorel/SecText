# SecText

SecText (SecureText) is a beginner-friendly cybersecurity app built with Python and CustomTkinter.
It focuses on a clean, modern desktop interface with modular code that can be extended later.

## Features

- AES-based text encryption and decryption using the `cryptography` library
- File encryption and decryption
- SHA-256 hash generation
- Password generator with customizable length

## Project Structure

```text
main.py
gui/
crypto/
utils/
assets/
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes

- The app uses Fernet from `cryptography`, which provides AES-backed symmetric encryption.
- Example icon placeholders are included in `assets/icons/` as SVG files.