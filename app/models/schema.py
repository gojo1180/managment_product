from pydantic import BaseModel, Field
from typing import Optional

class ProductManualCreate(BaseModel):
    """Model untuk input manual lengkap"""
    name: str = Field(..., min_length=1)
    category_name: str
    stock: int = Field(default=0, ge=0)
    description: Optional[str] = None
    barcode: Optional[str] = None # Jika kosong, akan di-generate otomatis

class BarcodeScanRequest(BaseModel):
    """Model untuk input barcode saja"""
    barcode: str