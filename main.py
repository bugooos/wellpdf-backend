from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from converters import ALL_ROUTERS

app = FastAPI(title="WellPDF Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all converters
for router in ALL_ROUTERS:
    app.include_router(router)
