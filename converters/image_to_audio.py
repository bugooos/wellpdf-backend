from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import wave
import shutil
import os
import struct

from core.utils import temp_input_path, safe_output_path

router = APIRouter()
CHUNK = 8192


@router.post("/convert/image-to-audio", summary="Image to Audio (Lossless Container)")
async def image_to_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    ext = os.path.splitext(file.filename)[1].lstrip(".").lower()
    if not ext:
        raise HTTPException(status_code=400, detail="Unknown image extension")

    input_path = temp_input_path("bin")
    output_path = safe_output_path(file.filename, "wav")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        size = os.path.getsize(input_path)
        ext_bytes = ext.encode("ascii")

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(1)     # 8-bit container (not audio!)
            wf.setframerate(8000)

            # Write header
            wf.writeframes(struct.pack("<Q", size))
            wf.writeframes(struct.pack("B", len(ext_bytes)))
            wf.writeframes(ext_bytes)

            # Stream raw bytes
            with open(input_path, "rb") as img:
                while True:
                    chunk = img.read(CHUNK)
                    if not chunk:
                        break
                    wf.writeframes(chunk)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="audio/wav"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
