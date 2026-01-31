# engine/types.py

def normalize(ext: str) -> str:
    return ext.lower().strip(".")

SUPPORTED_EXTS = {
    "pdf","doc","docx","odt","rtf",
    "txt","md","csv","json","xml",
    "html","log",
    "xls","xlsx","ods",
    "ppt","pptx","odp",
    "epub"
}
