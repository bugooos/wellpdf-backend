from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import shutil
import os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/xlsx-to-csv", summary="Convert XLSX to CSV")
async def xlsx_to_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only XLSX files allowed")

    input_path = temp_input_path("xlsx")
    output_path = safe_output_path(file.filename, "csv")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        df = pd.read_excel(input_path)
        df.to_csv(output_path, index=False)

        return FileResponse(output_path, filename=os.path.basename(output_path))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
