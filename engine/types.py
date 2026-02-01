import os
from engine.core.ingest import ingest
from engine.core.emit import emit
from engine.core.types import normalize, SUPPORTED_EXTS

def run_conversion(input_path: str, from_ext: str, to_ext: str, output_path: str):
    from_ext = normalize(from_ext)
    to_ext = normalize(to_ext)

    if from_ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported input format: {from_ext}")

    if to_ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported output format: {to_ext}")

    kind, data = ingest(input_path, from_ext)
    emit(kind, data, output_path, to_ext)
