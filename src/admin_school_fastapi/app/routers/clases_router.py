from fastapi import APIRouter, Depends, HTTPException
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.services import clases_service as crud_clase
from admin_school_fastapi.app.schemas.clases_schema import ClaseCreate, ClaseResponse
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db

router = APIRouter(prefix="/clases", tags=["Clases"])


## registro de clases
@router.post("/", response_model=ClaseResponse)
def registrar_clase(input:ClaseCreate, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} registra clase")
    if not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para crear clases - Solo docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_clase.create_clase(db, input, current_user.docente_id)

# Listado de clases
@router.get("/", response_model=list[ClaseResponse])
def listar_clases(skip: int = 0, limit: int = 10, curso_id: int = 0, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} consulta clases")
    if not usuario.is_admin() and not usuario.is_director():
        logger.info(f"Usuario {usuario.email} no tiene permiso para consultar clases - Solo Admin o Director")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_clase.get_clases(db, skip=skip, limit=limit, curso_id=curso_id)

@router.get("/by_docente")
def get_clases_by_docente( current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta clases del docente")
    if not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar clases del docente - Solo docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_clase.get_clases_by_docente(db, docente_id=current_user.docente_id)

# Eliminacion de clases
@router.delete("/{clase_id}")
def eliminar_clase(clase_id: int, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} elimina clase id: {clase_id}")
    if not usuario.is_docente():
        logger.info(f"Usuario {usuario.email} no tiene permiso para eliminar clases - Solo docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_clase.delete_clase(db, clase_id=clase_id)