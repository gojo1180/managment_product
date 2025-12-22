from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.API_produk import router as product_router
from app.api.API_auth import router as auth_router
import uvicorn


app = FastAPI(
    title="Sistem Manajemen Inventaris",
    description="API Backend untuk mengelola stok barang melalui input manual dan scan barcode menggunakan Supabase.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Mengizinkan semua origin
    allow_credentials=False,   # Ubah ke False jika menggunakan "*"
    allow_methods=["*"],      # Mengizinkan semua method (GET, POST, PATCH, dll)
    allow_headers=["*"],      # Mengizinkan semua header
)

# Inisialisasi Aplikasi FastAPI
# Kita memberikan metadata agar tampilan /docs (Swagger UI) lebih informatif
# Global Exception Handler
# Menangkap error tak terduga agar aplikasi tidak langsung mati dan memberikan pesan JSON yang rapi
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Terjadi kesalahan internal pada server", "detail": str(exc)},
    )

# Mendaftarkan Router dari app/api/products.py
# Ini akan menggabungkan semua endpoint yang kita buat di file terpisah ke aplikasi utama
app.include_router(product_router)
app.include_router(auth_router)

@app.get("/", tags=["Health Check"])
def health_check():
    """Endpoint dasar untuk memastikan server berjalan dengan baik"""
    return {
        "status": "Running",
        "mode": "Zero Auth",
        "docs": "/docs"
    }

if __name__ == "__main__":
    # Menjalankan server menggunakan Uvicorn
    # host 0.0.0.0 memungkinkan akses dari perangkat lain dalam jaringan yang sama (berguna saat tes scan via HP)
    # reload=True akan merestart server otomatis setiap kali kamu mengubah kode
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)