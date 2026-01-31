# engine/router.py

from engine.ingest import ingest
from engine.emit import emit
from engine.types import normalize, SUPPORTED_EXTS


def convert(input_path, from_ext, to_ext, out_path):
    from_ext = normalize(from_ext)
    to_ext = normalize(to_ext)

    # 1️⃣ Validate formats
    if from_ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported input format: {from_ext}")

    if to_ext not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported output format: {to_ext}")

    # 2️⃣ Ingest ONCE → canonical
    kind, data = ingest(input_path, from_ext)

    # 3️⃣ Emit ONCE → final format
    emit(kind, data, out_path, to_ext)
