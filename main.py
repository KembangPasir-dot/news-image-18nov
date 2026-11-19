"""Copy the bundled entry.png to /output/entry.png."""

import os
import shutil
import hashlib
from pathlib import Path

IMAGE_NAME = "entry.png"

BASE_DIR = Path(__file__).resolve().parent
SRC = BASE_DIR / IMAGE_NAME
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> tuple[Path, int, str]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / IMAGE_NAME
    shutil.copyfile(SRC, destination)

    if not destination.is_file():
        raise FileNotFoundError(f"Copied file is missing: {destination}")
    size = destination.stat().st_size
    if size != SRC.stat().st_size:
        raise ValueError(f"Copied file has the wrong size: {destination}")

    with SRC.open("rb") as source_file, destination.open("rb") as copied_file:
        source_hash = hashlib.file_digest(source_file, "sha256").hexdigest()
        copied_hash = hashlib.file_digest(copied_file, "sha256").hexdigest()
    if copied_hash != source_hash:
        raise ValueError(f"Copied file has a different SHA-256: {destination}")

    return destination, size, copied_hash


if __name__ == "__main__":
    path, size, sha256 = main()
    print(f"{path.name}: {size} bytes, SHA-256 {sha256}")
