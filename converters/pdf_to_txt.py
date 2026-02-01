from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os

from core.utils import temp_input_path, safe_output_path
from pdfminer.high_level import extract_text

router = APIRouter()

@router.post("/convert/pdf-to-txt", summary="Convert PDF to TXT")
async def pdf_to_txt(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = temp_input_path("pdf")
    output_path = safe_output_path(file.filename, "txt")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = extract_text(input_path)

        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in PDF"
            )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
