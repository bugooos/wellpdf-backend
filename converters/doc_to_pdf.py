from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os, subprocess, sys

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

def libreoffice_cmd():
    return "soffice" if sys.platform.startswith("win") else "libreoffice"

@router.post("/convert/doc-to-pdf", summary="Convert DOC to PDF")
async def doc_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".doc"):
        raise HTTPException(status_code=400, detail="Only DOC files allowed")

    input_path = temp_input_path("doc")

    # IMPORTANT: output_dir, not output_file
    output_dir = os.path.dirname(input_path)
    final_output = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        subprocess.run(
            [
                libreoffice_cmd(),
                "--headless",
                "--convert-to",
                "pdf",
                input_path,
                "--outdir",
                output_dir
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # LibreOffice output name (same base name)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        generated_pdf = os.path.join(output_dir, base_name + ".pdf")

        if not os.path.exists(generated_pdf):
            raise RuntimeError("LibreOffice did not generate PDF")

        # Rename to your desired output path
        shutil.move(generated_pdf, final_output)

        return FileResponse(
            final_output,
            filename=os.path.basename(final_output),
            media_type="application/pdf"
        )

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="LibreOffice conversion failed")

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
