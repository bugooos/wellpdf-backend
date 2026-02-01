from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/txt-to-pdf", summary="Convert TXT to PDF")
async def txt_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only TXT files allowed")

    input_path = temp_input_path("txt")
    output_path = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        y = height - 40

        with open(input_path, "r", encoding="utf-8") as f:
            for line in f:
                if y < 40:
                    c.showPage()
                    y = height - 40
                c.drawString(40, y, line.strip())
                y -= 14

        c.save()
        return FileResponse(output_path, filename=os.path.basename(output_path))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
