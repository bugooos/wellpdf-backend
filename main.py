from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.temp_cleanup import start_temp_cleanup

from converters import ALL_ROUTERS

app = FastAPI(title="WellPDF Backend")
start_temp_cleanup()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://wellpdf.pages.dev",
        "https://wellpdf.in",
        "https://www.wellpdf.in"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in ALL_ROUTERS:
    app.include_router(router)