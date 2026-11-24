"""Writes the entry line for the make.fun bounty "Status Report Comedy Sprint".

The program holds the line in the ENTRY constant, validates it, and writes it as
UTF-8 to entry.txt in $MAKEFUN_OUTPUT_DIR (default /output). It reads no clock
and no randomness, so every run produces identical bytes.
"""

import os
import sys

ENTRY = (
    "Delivered 9 of 10 items. The tenth was deleted by me at 4pm to protect it "
    "from being asked about again."
)

OUTPUT_DIR_ENV = "MAKEFUN_OUTPUT_DIR"
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.txt"


def validate_entry(text) -> str | None:
    """Return None if text is a usable entry line, otherwise an error message."""
    if not isinstance(text, str):
        return "entry must be a str"
    if not text.strip():
        return "entry is blank"
    if not 1 <= len(text) <= 200:
        return "entry must be 1 to 200 code points"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    if text != text.strip():
        return "entry must not have leading or trailing whitespace"
    return None


def main() -> int:
    entry = ENTRY
    error = validate_entry(entry)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    out_dir = os.environ.get(OUTPUT_DIR_ENV, DEFAULT_OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, OUTPUT_NAME)

    payload = entry + chr(10)
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(payload)

    with open(out_path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != payload.encode("utf-8"):
        print("readback mismatch: file does not match the intended bytes", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
