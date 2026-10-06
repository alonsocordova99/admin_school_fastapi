
from fastapi import APIRouter, Depends, HTTPException
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.schemas.curso_schema import CourseCreate, CourseResponse, PeriodoCreate, PeriodoResponse, AsignarDocenteCreate
from admin_school_fastapi.app.services import cursos_services as crud_curso
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db


router = APIRouter(prefix="/cursos", tags=["Cursos"])


## registro de periodos
@router.post("/periodo", response_model=PeriodoResponse)
def registrar_periodo(input:PeriodoCreate, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} registra periodo")
    if not current_user.is_admin():
        logger.info(f"Usuario {current_user.email} no tiene permiso para crear periodos - Solo Admin")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.create_period(db, input)

@router.get("/periodo", response_model=list[PeriodoResponse])
def listar_periodos(skip: int = 0, limit: int = 10, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta periodos")
    return crud_curso.get_periods(db, skip=skip, limit=limit)

## registro de cursos
@router.post("/", response_model=CourseResponse)
def registrar_curso(input:CourseCreate, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} registra curso")
    if not current_user.is_admin() and not current_user.is_director():
        logger.info(f"Usuario {current_user.email} no tiene permiso para crear cursos - Solo Admin o Director")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.create_course(db, input, current_user)
    
## listado de cursos
@router.get("/", response_model=list[CourseResponse])
def listar_cursos(
    skip: int = 0, 
    limit: int = 10, 
    periodo_id: int = 0, 
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    logger.info(f"Usuario {current_user.email} consulta cursos")
    if not current_user.is_admin() and not current_user.is_director():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar cursos - Solo Admin o Director")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.get_courses(db, skip=skip, limit=limit,periodo_id=periodo_id)
    
@router.get("/by_docente")
def get_cursos_by_docente( current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta cursos del docente")
    if not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar cursos del docente - Solo docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.get_cursos_by_docente(db, docente_id=current_user.docente_id)

@router.get("/by_estudiante")
def get_cursos_by_estudiante( current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta cursos del estudiante")
    if not current_user.is_estudiante():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar cursos del estudiante - Solo estudiante")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.get_cursos_by_estudiante(db, estudiante_id=current_user.estudiante_id)

@router.get("/{curso_id}")
def get_curso(curso_id: int, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta curso id: {curso_id}")
    if not current_user.is_admin() and not current_user.is_director() and not current_user.is_docente():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar cursos - Solo Admin, Director o Docente")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.get_curso_detalle(db, curso_id=curso_id, rol=current_user.rol_id)

@router.delete("/{curso_id}")
def eliminar_curso(curso_id: int, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {curso_id} elimina curso id: {curso_id}")
    if not current_user.is_admin() and not current_user.is_director():
        logger.info(f"Usuario {current_user.email} no tiene permiso para eliminar cursos - Solo Admin o Director")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.delete_course(db, curso_id=curso_id)


@router.put("/asignar_docente")
def actualizar_curso(input: AsignarDocenteCreate,  current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} asigna docente a curso")
    if not current_user.is_admin() and not current_user.is_director():
        logger.info(f"Usuario {current_user.email} no tiene permiso para asignar docente a curso - Solo Admin o Director")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return crud_curso.asignar_docente(db, input=input)

