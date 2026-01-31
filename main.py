from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import uuid
import os
import shutil

from engine.router import convert

app = FastAPI()

# ✅ CORS (required for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = "temp"
os.makedirs(BASE, exist_ok=True)


@app.post("/convert")
async def convert_api(
    file: UploadFile,
    from_ext: str = Form(...),
    to_ext: str = Form(...)
):
    # ✅ DEBUG LOGS (NOW CORRECT)
    print("REQUEST RECEIVED")
    print("Filename:", file.filename)
    print("from_ext:", from_ext)
    print("to_ext:", to_ext)

    uid = str(uuid.uuid4())
    input_path = f"{BASE}/{uid}.{from_ext}"
    output_path = f"{BASE}/{uid}.{to_ext}"

    # Save uploaded file
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Convert with safety
    try:
        convert(input_path, from_ext, to_ext, output_path)
    except Exception as e:
        print("CONVERSION ERROR:", e)
        raise HTTPException(status_code=400, detail="Conversion failed")

    # Return file to frontend
    return FileResponse(
        output_path,
        filename=f"converted.{to_ext}",
        media_type="application/octet-stream"
    )
