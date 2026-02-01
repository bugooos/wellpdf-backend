from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import shutil
import os

from core.utils import temp_input_path, safe_output_path

router = APIRouter()

@router.post("/convert/csv-to-xlsx", summary="Convert CSV to XLSX")
async def csv_to_xlsx(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    input_path = temp_input_path("csv")
    output_path = safe_output_path(file.filename, "xlsx")

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        df = pd.read_csv(input_path)
        df.to_excel(output_path, index=False)

        return FileResponse(
            output_path,
            filename=os.path.basename(output_path),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
