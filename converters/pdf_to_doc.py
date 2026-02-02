from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os

from pdfminer.high_level import extract_text
from docx import Document

from core.utils import temp_input_path, safe_output_path

router = APIRouter()


@router.post("/convert/pdf-to-doc", summary="Convert PDF to DOC")
async def pdf_to_doc(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = temp_input_path("pdf")
    output_path = safe_output_path(file.filename, "doc")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # 1️⃣ Extract text from PDF
        text = extract_text(input_path)
        if not text or not text.strip():
            raise RuntimeError("No extractable text found in PDF")

        # 2️⃣ Create DOC
        doc = Document()
        for line in text.splitlines():
            doc.add_paragraph(line)

        doc.save(output_path)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="application/msword"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
