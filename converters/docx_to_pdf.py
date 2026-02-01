from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os
from docx2pdf import convert
from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/docx-to-pdf", summary="Convert DOCX to PDF")
async def docx_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(400, "Only DOCX files allowed")

    input_path = temp_input_path("docx")
    output_path = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    convert(input_path, output_path)

    return FileResponse(output_path, filename=os.path.basename(output_path))
