from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PyPDF2 import PdfReader
from PIL import Image, ImageDraw
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/pdf-to-jpg", summary="Convert PDF to JPG")
async def pdf_to_jpg(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    input_path = temp_input_path("pdf")
    output_path = safe_output_path(file.filename, "jpg")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        reader = PdfReader(input_path)

        img = Image.new("RGB", (1200, 1600), "white")
        draw = ImageDraw.Draw(img)

        y = 40
        for page in reader.pages:
            text = page.extract_text()
            if text:
                for line in text.split("\n"):
                    draw.text((40, y), line, fill="black")
                    y += 20
                y += 40

        img.save(output_path, "JPEG", quality=95)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="image/jpeg"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
