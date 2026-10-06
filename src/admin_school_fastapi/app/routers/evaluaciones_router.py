
from fastapi import APIRouter, Depends, HTTPException
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.services import evaluaciones_service as crud_evaluacion
from admin_school_fastapi.app.schemas.evaluacion_schema import EvaluacionCreate, EvaluacionResponse, EvaluacionWithDetails
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db


router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])

## registro de evaluaciones
@router.post("/", response_model=EvaluacionResponse)
def registrar_evaluacion(input:EvaluacionCreate, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} registra evaluacion")
    if not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para crear evaluaciones - Solo docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")

    return crud_evaluacion.create_evaluacion(db, input, current_user.docente_id)
    
@router.get("/", response_model=list[EvaluacionWithDetails])
def lista_evaluaciones(skip: int = 0, limit: int = 10, clase_id: int = 0, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta evaluaciones")
    return crud_evaluacion.get_evaluaciones(db, skip=skip, limit=limit, clase_id=clase_id)


    
@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(evaluacion_id: int, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {evaluacion_id} elimina evaluacion id: {evaluacion_id}")
    if not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para eliminar evaluaciones - Solo docente")
    return crud_evaluacion.delete_evaluacion(db, evaluacion_id=evaluacion_id)
