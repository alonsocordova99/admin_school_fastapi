
from admin_school_fastapi.app.schemas.curso_schema import CourseCreate, PeriodoCreate, AsignarDocenteCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from admin_school_fastapi.app.db.models.curso_model import Curso
from admin_school_fastapi.app.db.models.periodo_model import Periodo
from admin_school_fastapi.app.schemas import ApiReponseSchema
from admin_school_fastapi.app.db.models.usuario_model import Usuario, RoleEnum
from admin_school_fastapi.app.db.models.docente_model import Docente
from admin_school_fastapi.app.core.utils.logging_config import logger
from sqlalchemy.orm import Session

##-------------------------------
## PERIODOS
##-------------------------------
def get_periods(db:Session, skip: int = 0, limit: int = 10):
    logger.info(f"Consulta periodos skip: {skip} limit: {limit}")
    return db.query(Periodo).offset(skip).limit(limit).all()

def create_period(db:Session, input: PeriodoCreate) -> Periodo:
    new_period = Periodo(
        nombre=input.nombre,
        fecha_inicio=input.fecha_inicio,
        fecha_fin=input.fecha_fin
    )
    db.add(new_period)
    db.commit()
    db.refresh(new_period)
    logger.info(f"Periodo creado correctamente id: {new_period.id} nombre: {new_period.nombre}")
    return new_period


##-------------------------------
## CURSOS
##-------------------------------
def get_courses(db:Session, skip: int, limit: int, periodo_id:int):
    if not periodo_id:
        logger.info(f"Periodo id no proporcionado")
        return db.query(Curso).offset(skip).limit(limit).all()
    period = db.query(Periodo).filter(Periodo.id == periodo_id).first()
    if not period:
        logger.info(f"Periodo no encontrado id: {periodo_id}")
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    logger.info(f"Consulta cursos del periodo id: {periodo_id} skip: {skip} limit: {limit}")
    return db.query(Curso).filter(Curso.periodo_id == periodo_id).offset(skip).limit(limit).all()
        
def get_cursos_by_docente(db:Session, docente_id: int):
    logger.info(f"Consulta cursos del docente id: {docente_id}")
    cursos_db = db.query(Curso).filter(Curso.docente_id == docente_id).all()
    return cursos_db
    
def get_cursos_by_estudiante(db:Session, estudiante_id: int):
    logger.info(f"Consulta cursos del estudiante id: {estudiante_id}")
    return db.query(Curso).filter(Curso.matriculas.any(estudiante_id=estudiante_id)).all()
    
def get_curso_detalle(db:Session, curso_id:int, rol: RoleEnum):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        logger.info(f"Curso no encontrado id: {curso_id}")
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    dto_curso = {
        "id": curso.id,
        "nombre": curso.nombre,
        "descripcion": curso.descripcion,
        "grado": curso.grado,
        "seccion": curso.seccion,
        "periodo_id": curso.periodo_id,
        "matriculas": [],
        "clases": []
    }
    for matricula in curso.matriculas:
        dto_curso["matriculas"].append({
            "id": matricula.id,
            "fecha_registro": matricula.fecha_registro,
            "estudiante_id": matricula.estudiante_id,
            "nombre_estudiante": matricula.estudiante.nombre_completo
        })
            
    for clase in curso.clases:
        dto_curso["clases"].append({
            "id": clase.id,
            "nombre": clase.nombre,
            "descripcion": clase.descripcion,
            "fecha_inicio": clase.fecha_inicio,
            "fecha_fin": clase.fecha_fin,
            "link_meeting": clase.link_meeting,
            "link_video": clase.link_video,
            "evaluaciones": clase.evaluaciones
        })
    logger.info(f"Curso consultado correctamente id: {curso.id} nombre: {curso.nombre}")
    return dto_curso
 
    
def create_course(db:Session,input: CourseCreate, user: Usuario):
        new_course = Curso(
            nombre=input.nombre,
            descripcion=input.descripcion,
            grado=input.grado,
            seccion=input.seccion,
            docente_id=input.docente_id,
            periodo_id=input.periodo_id
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        logger.info(f"Curso creado correctamente id: {new_course.id} nombre: {new_course.nombre}")
        return new_course

def delete_course(db:Session, curso_id: int):
        db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
        if db_curso:
            db.delete(db_curso)
            db.commit()
            logger.info(f"Curso eliminado correctamente id: {curso_id}")
        else:
            logger.info(f"Curso no encontrado id: {curso_id}")
            raise HTTPException(status_code=404, detail="Curso no encontrado")  
        return ApiReponseSchema(
            status_code=200,
            success=True,
            mensaje="Curso eliminado correctamente"
        )

def asignar_docente(db:Session,input: AsignarDocenteCreate):
    curso = db.query(Curso).filter(Curso.id == input.curso_id).first()
    if not curso:
        logger.info(f"Curso no encontrado id: {input.curso_id}")
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    docente = db.query(Docente).filter(Docente.id == input.docente_id).first()
    if not docente:
        logger.info(f"Docente no encontrado id: {input.docente_id}")
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    
    if curso.docente_id == docente.id:
        logger.info(f"Docente {docente.nombre_completo} ya dicta el curso id: {input.curso_id}")
        raise HTTPException(status_code=404, detail="Docente ya dicta el curso")

    curso.docente_id = input.docente_id
    db.commit()
    db.refresh(curso)
    logger.info(f"Curso actualizado correctamente id: {curso.id} nombre: {curso.nombre},docente_id: {curso.docente_id}")
    return {
        "status_code": 200,
        "success": True,
        "mensaje": "Curso actualizado correctamente"
    }