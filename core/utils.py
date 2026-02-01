import os
import uuid
from pathlib import Path

TEMP_DIR = "temp"

def ensure_temp():
    os.makedirs(TEMP_DIR, exist_ok=True)

def temp_input_path(ext: str) -> str:
    ensure_temp()
    return os.path.join(TEMP_DIR, f"{uuid.uuid4()}.{ext}")

def safe_output_path(original_name: str, new_ext: str) -> str:
    """
    Creates output path using original filename.
    Adds (1), (2) if file already exists.
    """
    ensure_temp()

    base = Path(original_name).stem
    filename = f"{base}.{new_ext}"
    path = Path(TEMP_DIR) / filename

    counter = 1
    while path.exists():
        filename = f"{base}({counter}).{new_ext}"
        path = Path(TEMP_DIR) / filename
        counter += 1

    return str(path)
