
from fastapi import APIRouter, Depends, HTTPException
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.schemas.matricula_schema import MatriculaCreate, MatriculaResponse
from admin_school_fastapi.app.services import matriculas_services as crud_matricula
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db

router = APIRouter(prefix="/matriculas", tags=["Matriculas"])

## registro de matriculas
@router.post("/", response_model=MatriculaResponse)
def registrar_matricula(input:MatriculaCreate, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} registra matricula")
    if not usuario.is_admin():
        logger.info(f"Usuario {usuario.email} no tiene permiso para crear matriculas - solo Admin")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_matricula.create_matricula(db, input)
    
#------------------------------------------
# Listado de matriculas
# -------------------------------------------
@router.get("/", response_model=list[MatriculaResponse])
def listar_matriculas(
    skip: int = 0, 
    limit: int = 10, 
    curso_id: int = 0,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    logger.info(f"Usuario {current_user.email} consulta matriculas")
    if not current_user.is_admin() and not current_user.is_director() and not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar matriculas - Solo Admin, Director o Docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_matricula.get_matriculas(db, skip=skip, limit=limit, curso_id=curso_id)

@router.get("/by_estudiante/{estudiante_id}", response_model=list[MatriculaResponse])
def get_matriculas_by_estudiante(estudiante_id: int, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta matriculas del estudiante - id: {estudiante_id}")
    return crud_matricula.get_matriculas_by_estudiante(db, estudiante_id=estudiante_id)
    
@router.delete("/{matricula_id}")
def delete_matricula(matricula_id: int, db = Depends(get_db)):
    logger.info(f"Usuario {matricula_id} elimina matricula id: {matricula_id}")
    return crud_matricula.delete_matricula(db, matricula_id=matricula_id)