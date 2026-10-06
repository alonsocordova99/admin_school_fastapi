from pydantic import BaseModel
from typing import Optional
from datetime import date

class CourseCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    grado: str
    seccion: str
    docente_id: Optional[int] = None
    periodo_id: int

class CourseResponse(CourseCreate):
    id: int
    class Config:
        from_attributes = True

class PeriodoCreate(BaseModel):
    nombre: str
    fecha_inicio: date
    fecha_fin: date

class PeriodoResponse(PeriodoCreate):
    id: int
    class Config:
        from_attributes = True

class AsignarDocenteCreate(BaseModel):
    docente_id: int
    curso_id: int