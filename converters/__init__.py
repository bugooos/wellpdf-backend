import platform

# Always-safe routers (pure Python / light deps)
from .csv_to_xlsx import router as csv_to_xlsx_router
from .docx_to_txt import router as docx_to_txt_router
from .docx_to_xlsx import router as docx_to_xlsx_router
from .pdf_to_txt import router as pdf_to_txt_router
from .txt_to_docx import router as txt_to_docx_router
from .txt_to_pdf import router as txt_to_pdf_router
from .xlsx_to_csv import router as xlsx_to_csv_router
from .doc_to_pdf import router as doc_to_pdf_router
from .docx_to_pdf import router as docx_to_pdf_router
from .pdf_to_doc import router as pdf_to_doc_router
from .pdf_to_docx import router as pdf_to_docx_router
from .pdf_to_html import router as pdf_to_html_router
from .png_to_pdf import router as png_to_pdf_router
from .jpg_to_pdf import router as jpg_to_pdf_router
from .pdf_to_pptx import router as pdf_to_pptx_router

ALL_ROUTERS = [
    csv_to_xlsx_router,
    docx_to_txt_router,
    docx_to_xlsx_router,
    pdf_to_txt_router,
    txt_to_docx_router,
    txt_to_pdf_router,
    xlsx_to_csv_router,
    doc_to_pdf_router,
    docx_to_pdf_router,
    pdf_to_doc_router,
    pdf_to_docx_router,
    pdf_to_html_router,
    png_to_pdf_router,
    jpg_to_pdf_router,
    pdf_to_pptx_router,
]

# ==================================================
# Linux-only converters (WeasyPrint / Libre / GTK)
# ==================================================
if platform.system() == "Linux":
    from .pdf_to_pptx import router as pdf_to_pptx_router
    from .pptx_to_pdf import router as pptx_to_pdf_router

    ALL_ROUTERS.extend([
        pdf_to_pptx_router,
        pptx_to_pdf_router,
    ])
