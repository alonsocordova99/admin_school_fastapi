from pydantic import BaseModel
from datetime import date

class MatriculaCreate(BaseModel):
    estudiante_id: int
    curso_id: int

class MatriculaResponse(MatriculaCreate):
    id: int
    fecha_registro: date
    class Config:
        from_attributes = True