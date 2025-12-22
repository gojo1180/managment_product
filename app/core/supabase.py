import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

# Ambil kredensial dari environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di file .env")

# Inisialisasi client tunggal untuk digunakan di seluruh aplikasi
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)