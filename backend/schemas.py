from pydantic import BaseModel, Field
from typing import Optional

# Menangani validasi payload dari front-end
class M2CreateRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Judul tidak boleh kosong")
    description: Optional[str] = None

class M2Response(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    user_id: str

    class Config:
        from_attributes = True