from .csv_to_xlsx import router as csv_to_xlsx_router
from .docx_to_pdf import router as docx_to_pdf_router

ALL_ROUTERS = [
    csv_to_xlsx_router,
    docx_to_pdf_router,
]
