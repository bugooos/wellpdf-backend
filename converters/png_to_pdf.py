from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/png-to-pdf", summary="Convert PNG to PDF")
async def png_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".png"):
        raise HTTPException(status_code=400, detail="Only PNG files allowed")

    input_path = temp_input_path("png")
    output_path = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        img = Image.open(input_path).convert("RGB")
        img.save(output_path, "PDF")

        return FileResponse(output_path, filename=os.path.basename(output_path))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
