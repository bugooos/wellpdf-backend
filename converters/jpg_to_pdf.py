from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import shutil, os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/jpg-to-pdf", summary="Convert JPG to PDF (Fit Page)")
def jpg_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Only JPG files allowed")

    input_path = temp_input_path("jpg")
    output_path = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        img = Image.open(input_path).convert("RGB")

        # Get image size in pixels
        width_px, height_px = img.size

        # Get DPI (fallback to 72)
        dpi = img.info.get("dpi", (72, 72))
        dpi_x, dpi_y = dpi

        # Convert pixels → points
        width_pt = width_px * 72 / dpi_x
        height_pt = height_px * 72 / dpi_y

        # Save PDF with exact page size
        img.save(
            output_path,
            "PDF",
            resolution=72,
            save_all=True,
            append_images=[],
            page_size=(width_pt, height_pt)
        )

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="application/pdf"
        )

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
