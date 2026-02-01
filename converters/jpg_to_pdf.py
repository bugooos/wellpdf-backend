from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/jpg-to-pdf", summary="Convert JPG to PDF")
async def jpg_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only JPG/JPEG files allowed")

    input_path = temp_input_path("jpg")
    output_path = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        img = Image.open(input_path).convert("RGB")
        img.save(output_path, "PDF", resolution=300)

        return FileResponse(output_path, filename=os.path.basename(output_path))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
