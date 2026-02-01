from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from docx import Document
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/txt-to-docx", summary="Convert TXT to DOCX")
async def txt_to_docx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only TXT files allowed")

    input_path = temp_input_path("txt")
    output_path = safe_output_path(file.filename, "docx")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        doc = Document()
        with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                doc.add_paragraph(line.rstrip())

        doc.save(output_path)

        return FileResponse(output_path, filename=os.path.basename(output_path))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
