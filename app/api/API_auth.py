from fastapi import APIRouter, HTTPException
from app.models.auth import UserRegister, UserLogin
from app.core.supabase import supabase

# Inisialisasi router dengan prefix /auth
router = APIRouter(prefix="/auth", tags=["Autentikasi"])

@router.post("/register")
async def register(data: UserRegister):
    """Mendaftarkan pengguna baru ke Supabase Auth"""
    try:
        # Mengirim data pendaftaran ke Supabase
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {
                    "full_name": data.full_name
                }
            }
        })
        
        # Cek jika terjadi error dari sisi Supabase (seperti email sudah terdaftar)
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=400, detail=str(response.error.message))
            
        return {"message": "Registrasi berhasil! Silakan cek email untuk verifikasi jika diaktifkan."}
    except Exception as e:
        # Menangani error tak terduga
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Email sudah terdaftar.")
        raise HTTPException(status_code=400, detail=error_msg)

@router.post("/login")
async def login(data: UserLogin):
    """Masuk dan mendapatkan token JWT"""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email, 
            "password": data.password
        })
        
        # Mengembalikan data sesi agar bisa disimpan di frontend
        return {
            "access_token": response.session.access_token,
            "user_id": response.user.id,
            "email": response.user.email,
            "full_name": response.user.user_metadata.get("full_name")
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Email atau kata sandi salah.")