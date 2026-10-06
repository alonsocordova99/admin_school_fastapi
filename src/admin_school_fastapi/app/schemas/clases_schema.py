
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ClaseCreate(BaseModel):
    nombre: str
    curso_id: int
    descripcion: str | None = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    link_meeting: Optional[str] = None
    link_video: Optional[str] = None
    
class ClaseResponse(ClaseCreate):
    id: int
    class Config:
        from_attributes = True