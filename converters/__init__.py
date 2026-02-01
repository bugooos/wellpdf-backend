from .csv_to_xlsx import router as csv_to_xlsx_router
from .docx_to_txt import router as docx_to_txt_router
from .docx_to_xlsx import router as docx_to_xlsx_router
from .pdf_to_txt import router as pdf_to_txt_router
from .txt_to_docx import router as txt_to_docx_router
from .txt_to_pdf import router as txt_to_pdf_router
from .xlsx_to_csv import router as xlsx_to_csv_router


ALL_ROUTERS = [
   csv_to_xlsx_router,
   docx_to_txt_router,
   docx_to_xlsx_router,
   pdf_to_txt_router,
   txt_to_pdf_router,
   xlsx_to_csv_router,
   txt_to_docx_router,
]
