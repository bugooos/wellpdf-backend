from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os
from pdf2docx import Converter
from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/pdf-to-docx", summary="Convert PDF to DOCX")
async def pdf_to_docx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    input_path = temp_input_path("pdf")
    output_path = safe_output_path(file.filename, "docx")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        return FileResponse(output_path, filename=os.path.basename(output_path))
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
