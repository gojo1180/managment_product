from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.API_produk import router as product_router
from app.api.API_auth import router as auth_router
import uvicorn

app = FastAPI(
    title="StokMaster Pro API",
    description="Sistem Manajemen Inventaris Backend",
    version="1.0.0"
)

# Pengaturan CORS yang mendukung Authorization Header di Produksi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handler untuk error global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Terjadi kesalahan pada server", "detail": str(exc)},
    )

app.include_router(product_router)
app.include_router(auth_router)

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Diperlukan untuk running lokal saja
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)