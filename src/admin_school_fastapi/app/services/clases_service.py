from admin_school_fastapi.app.db.models.clase_model import Clase
from admin_school_fastapi.app.db.models.curso_model import Curso
from fastapi import HTTPException
from admin_school_fastapi.app.schemas.clases_schema import ClaseCreate
from admin_school_fastapi.app.schemas import ApiReponseSchema
from admin_school_fastapi.app.core.utils.logging_config import logger
from sqlalchemy.orm import Session

def get_clases(db:Session, skip: int = 0, limit: int = 10, curso_id: int = 0):
    logger.info(f"Consulta clases skip: {skip} limit: {limit}")
    return db.query(Clase).offset(skip).limit(limit).all()
    
def get_clases_by_docente(db:Session, docente_id: int):
    logger.info(f"Consulta clases del docente id: {docente_id}")
    return db.query(Clase).join(Curso).filter(
        Curso.docente_id == docente_id
    ).all()
    

    
def create_clase(db:Session, input: ClaseCreate, docente_id: int):
    if not docente_id:
        logger.info(f"Docente id no proporcionado")
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    
    curso = db.query(Curso).filter(Curso.id == input.curso_id).first()
    if not curso:
        logger.info(f"Curso id no encontrado")
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    if curso.docente_id != docente_id:
        logger.info(f"Docente no dicta el curso")
        raise HTTPException(status_code=404, detail="Docente no dicta el curso")

    new_clase = Clase(
        nombre=input.nombre,
        curso_id=input.curso_id,
        descripcion=input.descripcion,
        fecha_inicio=input.fecha_inicio,
        fecha_fin=input.fecha_fin,
        link_meeting=input.link_meeting,
        link_video=input.link_video
    )
    db.add(new_clase)
    db.commit()
    db.refresh(new_clase)
    logger.info(f"Clase creada correctamente id: {new_clase.id} nombre: {new_clase.nombre}")
    return new_clase


def delete_clase(db:Session, clase_id: int):
    db_clase = db.query(Clase).filter(Clase.id == clase_id).first()
    if db_clase:
        logger.info(f"Clase eliminada correctamente id: {clase_id}")
        db.delete(db_clase)
        db.commit()
    else:
        logger.info(f"Clase no encontrada id: {clase_id}")
        raise HTTPException(status_code=404, detail="Clase no encontrado")
    return ApiReponseSchema(
        status_code=200,
        success=True,
        mensaje="Clase eliminado correctamente"
    )