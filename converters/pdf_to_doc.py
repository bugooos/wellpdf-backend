from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader
from docx import Document
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/pdf-to-doc", summary="Convert PDF to DOC (text)")
async def pdf_to_doc(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = temp_input_path("pdf")
    output_path = safe_output_path(file.filename, "doc")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        reader = PdfReader(input_path)
        doc = Document()

        for page in reader.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)

        doc.save(output_path)
        return FileResponse(output_path, filename=os.path.basename(output_path))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
