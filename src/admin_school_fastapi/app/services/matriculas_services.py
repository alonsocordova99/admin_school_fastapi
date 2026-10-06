
from admin_school_fastapi.app.schemas.matricula_schema import MatriculaCreate, MatriculaResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from admin_school_fastapi.app.schemas import ApiReponseSchema
from admin_school_fastapi.app.db.models.matricula_model import Matricula
from admin_school_fastapi.app.core.utils.logging_config import logger
from sqlalchemy.orm import Session

def get_matriculas(db:Session, skip: int = 0, limit: int = 10, curso_id: int = 0)-> list[MatriculaResponse]:
    if curso_id > 0:
        logger.info(f"Consulta matriculas del curso id: {curso_id} skip: {skip} limit: {limit}")
        return db.query(Matricula).filter(Matricula.curso_id == curso_id).offset(skip).limit(limit).all()
    logger.info(f"Consulta matriculas skip: {skip} limit: {limit}")
    return db.query(Matricula).offset(skip).limit(limit).all()
    
#------------------------------------------
# Registrar nueva matricula
# -------------------------------------------    
def create_matricula(db:Session, input: MatriculaCreate)-> Matricula:
    exit_matri = db.query(Matricula).filter(
            Matricula.estudiante_id == input.estudiante_id,
            Matricula.curso_id == input.curso_id
        ).first()
    if exit_matri:
        logger.info(f"Matricula ya existe id: {input.estudiante_id} curso_id: {input.curso_id}")
        raise HTTPException(status_code=400, detail="Matricula ya existe")
    
    new_matricula = Matricula(
        estudiante_id=input.estudiante_id,
        curso_id=input.curso_id
    )
    db.add(new_matricula)
    db.commit()
    db.refresh(new_matricula)
    logger.info(f"Matricula creada correctamente id: {new_matricula.id} estudiante: {new_matricula.nombre_estudiante} curso: {new_matricula.nombre_curso}")
    return new_matricula


def delete_matricula(db:Session, matricula_id: int):
    db_matricula = db.query(Matricula).filter(Matricula.id == matricula_id).first()
    if db_matricula:
        db.delete(db_matricula)
        db.commit()
        logger.info(f"Matricula eliminado correctamente id: {matricula_id}")
    else:
        logger.info(f"Matricula no encontrada id: {matricula_id}")
        raise HTTPException(status_code=404, detail="Matricula no encontrado")
    return ApiReponseSchema(
        status_code=200,
        success=True,
        mensaje="Matricula eliminado correctamente"
    )


def get_matriculas_by_estudiante(db:Session, estudiante_id: int):
    logger.info(f"Consulta matriculas del estudiante id: {estudiante_id}")
    return db.query(Matricula).filter(Matricula.estudiante_id == estudiante_id).all()