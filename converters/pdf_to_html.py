from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/pdf-to-html", summary="Convert PDF to HTML")
async def pdf_to_html(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = temp_input_path("pdf")
    output_path = safe_output_path(file.filename, "html")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        reader = PdfReader(input_path)

        html = [
            "<!DOCTYPE html>",
            "<html><head><meta charset='utf-8'>",
            "<title>Converted PDF</title>",
            "<style>body{font-family:Arial;line-height:1.6;padding:20px}</style>",
            "</head><body>"
        ]

        for page in reader.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    html.append(f"<p>{line}</p>")

        html.append("</body></html>")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="text/html"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
