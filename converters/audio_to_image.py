from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import wave
import shutil
import os
import struct

from core.utils import temp_input_path

router = APIRouter()
CHUNK = 8192
ALLOWED_EXTS = {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}


@router.post("/convert/audio-to-image", summary="Audio to Image (Exact Restore)")
async def audio_to_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only WAV files allowed")

    input_path = temp_input_path("wav")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        with wave.open(input_path, "rb") as wf:
            original_size = struct.unpack("<Q", wf.readframes(8))[0]
            ext_len = struct.unpack("B", wf.readframes(1))[0]
            ext = wf.readframes(ext_len).decode("ascii").lower()

            if ext not in ALLOWED_EXTS:
                raise HTTPException(status_code=400, detail="Invalid embedded image type")

            output_path = os.path.join(
                os.path.dirname(input_path),
                f"restored.{ext}"
            )

            written = 0
            with open(output_path, "wb") as out:
                while written < original_size:
                    chunk = wf.readframes(
                        min(CHUNK, original_size - written)
                    )
                    if not chunk:
                        break
                    out.write(chunk)
                    written += len(chunk)

        original_name = os.path.splitext(file.filename)[0]

        return FileResponse(
            output_path,
            filename=f"{original_name}.{ext}",
            media_type=f"image/{ext}"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
