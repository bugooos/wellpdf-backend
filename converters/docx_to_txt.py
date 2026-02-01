from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from docx import Document
import shutil, os
from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/docx-to-txt", summary="Convert DOCX to TXT")
async def docx_to_txt(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(400, "Only DOCX allowed")

    input_path = temp_input_path("docx")
    output_path = safe_output_path(file.filename, "txt")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc = Document(input_path)
    with open(output_path, "w", encoding="utf-8") as out:
        for p in doc.paragraphs:
            out.write(p.text + "\n")

    return FileResponse(output_path, filename=os.path.basename(output_path))
