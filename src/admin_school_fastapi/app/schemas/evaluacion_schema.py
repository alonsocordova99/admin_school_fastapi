
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from admin_school_fastapi.app.schemas.clases_schema import ClaseCreate
from admin_school_fastapi.app.schemas.matricula_schema import MatriculaCreate

class EvaluacionCreate(BaseModel):
    clase_id: int
    titulo: str
    descripcion: Optional[str] = None
    fecha: date

class EvaluacionResponse(EvaluacionCreate):
    id: int
    class Config:
        from_attributes = True


class ResultadoEvaluacionCreate(BaseModel):
    evaluacion_id: int
    matricula_id: int
    nota: float
    observaciones: Optional[str] = None

class ResultadoEvaluacionResponse(ResultadoEvaluacionCreate):
    id: int
    class Config:
        from_attributes = True



class EvaluacionWithDetails(EvaluacionResponse):
    detalles: List[ResultadoEvaluacionResponse] = []