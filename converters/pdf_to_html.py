from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os

from pdfminer.high_level import extract_text
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
        text = extract_text(input_path)

        if not text or not text.strip():
            raise RuntimeError("No extractable text found in PDF")

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{file.filename}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  white-space: pre-wrap;
  line-height: 1.6;
}}
</style>
</head>
<body>
{text}
</body>
</html>
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="text/html"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
