from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil, os, subprocess, platform

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

def get_libreoffice_cmd():
    if platform.system() == "Windows":
        return r"C:\Program Files\LibreOffice\program\soffice.exe"
    return "libreoffice"

@router.post("/convert/docx-to-pdf", summary="Convert DOCX to PDF")
async def docx_to_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only DOCX files allowed")

    input_path = temp_input_path("docx")
    output_dir = os.path.dirname(input_path)
    output_path = safe_output_path(file.filename, "pdf")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        libreoffice = get_libreoffice_cmd()

        if platform.system() == "Windows" and not os.path.exists(libreoffice):
            raise HTTPException(
                status_code=500,
                detail="LibreOffice not installed on server"
            )

        subprocess.run(
            [
                libreoffice,
                "--headless",
                "--convert-to",
                "pdf",
                input_path,
                "--outdir",
                output_dir,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # LibreOffice outputs: same name, .pdf
        generated_pdf = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        )

        if not os.path.exists(generated_pdf):
            raise HTTPException(status_code=500, detail="PDF conversion failed")

        os.replace(generated_pdf, output_path)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="application/pdf",
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
