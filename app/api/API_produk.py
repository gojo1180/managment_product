import random
import string
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Header, Depends
from app.models.schema import ProductManualCreate, BarcodeScanRequest
from app.core.supabase import supabase

router = APIRouter(prefix="/products", tags=["Products"])

# --- DEPENDENCY: VALIDASI USER ---
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Mengecek token JWT dan mengembalikan data user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Sesi tidak ditemukan. Silakan login kembali.")
    
    token = authorization.replace("Bearer ", "")
    try:
        # Memvalidasi token ke Supabase
        user_resp = supabase.auth.get_user(token)
        if not user_resp.user:
            raise HTTPException(status_code=401, detail="Sesi tidak valid.")
        return user_resp.user
    except Exception:
        raise HTTPException(status_code=401, detail="Token kadaluarsa atau tidak valid.")

def generate_unique_barcode():
    """Menghasilkan 12 digit angka unik"""
    while True:
        code = ''.join(random.choices(string.digits, k=12))
        check = supabase.table("products").select("id").eq("barcode", code).execute()
        if not check.data:
            return code

@router.get("/")
def get_all_products(authorization: str = Header(...), user = Depends(get_current_user)):
    # Mengeset context auth agar RLS di Supabase berfungsi (hanya ambil milik user ini)
    token = authorization.replace("Bearer ", "")
    supabase.postgrest.auth(token)
    
    response = supabase.table("products").select("*, categories(name)").execute()
    return response.data

@router.post("/scan")
def scan_barcode(request: BarcodeScanRequest, authorization: str = Header(...), user = Depends(get_current_user)):
    token = authorization.replace("Bearer ", "")
    supabase.postgrest.auth(token)
    
    result = supabase.table("products").select("*, categories(name)").eq("barcode", request.barcode).execute()
    if not result.data:
        return {"found": False, "barcode": request.barcode}
    return {"found": True, "data": result.data[0]}

@router.post("/manual")
def create_product_manual(data: ProductManualCreate, authorization: str = Header(...), user = Depends(get_current_user)):
    token = authorization.replace("Bearer ", "")
    supabase.postgrest.auth(token)

    # 1. Validasi Duplikasi Nama untuk user yang sama
    check_name = supabase.table("products").select("id").ilike("name", data.name).execute()
    if check_name.data:
        raise HTTPException(status_code=400, detail=f"Produk '{data.name}' sudah terdaftar di gudang anda.")

    # 2. Handle Barcode
    final_barcode = data.barcode or generate_unique_barcode()
    if data.barcode:
        check_bc = supabase.table("products").select("id").eq("barcode", final_barcode).execute()
        if check_bc.data:
            raise HTTPException(status_code=400, detail="Kode barcode ini sudah digunakan.")

    # 3. Handle Category (Get or Create)
    cat_query = supabase.table("categories").select("id").eq("name", data.category_name).execute()
    if not cat_query.data:
        new_cat = supabase.table("categories").insert({"name": data.category_name}).execute()
        category_id = new_cat.data[0]['id']
    else:
        category_id = cat_query.data[0]['id']

    # 4. Payload dengan user_id
    product_payload = {
        "name": data.name,
        "description": data.description,
        "stock": data.stock,
        "barcode": final_barcode,
        "category_id": category_id,
        "user_id": user.id # Identitas pemilik barang
    }
    
    result = supabase.table("products").insert(product_payload).execute()
    return {"status": "success", "data": result.data[0]}

@router.patch("/{product_id}")
def update_product(product_id: str, data: ProductManualCreate, authorization: str = Header(...), user = Depends(get_current_user)):
    token = authorization.replace("Bearer ", "")
    supabase.postgrest.auth(token)
    
    # Pastikan kategori ter-update jika berubah
    cat_query = supabase.table("categories").select("id").eq("name", data.category_name).execute()
    if not cat_query.data:
        new_cat = supabase.table("categories").insert({"name": data.category_name}).execute()
        category_id = new_cat.data[0]['id']
    else:
        category_id = cat_query.data[0]['id']

    update_payload = {
        "name": data.name,
        "description": data.description,
        "stock": data.stock,
        "category_id": category_id
    }
    
    result = supabase.table("products").update(update_payload).eq("id", product_id).execute()
    return {"status": "success", "data": result.data[0]}

@router.patch("/{product_id}/add-stock")
def add_stock(product_id: str, amount: int = Query(...), authorization: str = Header(...), user = Depends(get_current_user)):
    token = authorization.replace("Bearer ", "")
    supabase.postgrest.auth(token)
    
    current = supabase.table("products").select("stock").eq("id", product_id).execute()
    if not current.data:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    
    new_stock = current.data[0]['stock'] + amount
    if new_stock < 0: new_stock = 0
    
    supabase.table("products").update({"stock": new_stock}).eq("id", product_id).execute()
    return {"new_stock": new_stock}

@router.delete("/{product_id}")
def delete_product(product_id: str, authorization: str = Header(...), user = Depends(get_current_user)):
    token = authorization.replace("Bearer ", "")
    supabase.postgrest.auth(token)
    
    supabase.table("products").delete().eq("id", product_id).execute()
    return {"status": "success"}