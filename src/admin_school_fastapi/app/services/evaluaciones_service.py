from admin_school_fastapi.app.schemas.evaluacion_schema import EvaluacionCreate, EvaluacionResponse, ResultadoEvaluacionCreate, ResultadoEvaluacionResponse, EvaluacionWithDetails
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from admin_school_fastapi.app.schemas import ApiReponseSchema
from admin_school_fastapi.app.db.models.evaluacion_model import Evaluacion
from admin_school_fastapi.app.db.models.resultado_model import ResultadoEvaluacion
from admin_school_fastapi.app.db.models.clase_model import Clase
from admin_school_fastapi.app.core.utils.logging_config import logger
from sqlalchemy.orm import Session

def get_evaluaciones(db:Session, skip: int = 0, limit: int = 10, clase_id: int = 0) -> list[EvaluacionResponse]:
    if clase_id > 0:
        logger.info(f"Consulta evaluaciones del clase id: {clase_id} skip: {skip} limit: {limit}")
        return db.query(Evaluacion).filter(Evaluacion.clase_id == clase_id).offset(skip).limit(limit).all()
    logger.info(f"Consulta evaluaciones skip: {skip} limit: {limit}")
    return db.query(Evaluacion).offset(skip).limit(limit).all()
    
def get_evaluacion(db:Session, evaluacion_id: int) -> EvaluacionWithDetails:
    logger.info(f"Consulta evaluacion id: {evaluacion_id}")
    return db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    
def create_evaluacion(db:Session, input: EvaluacionCreate, docente_id: int) -> Evaluacion:
    if not docente_id:
        logger.info(f"Docente id no proporcionado")
        raise HTTPException(status_code=404, detail="Docente no encontrado")

    clase = db.query(Clase).filter(Clase.id == input.clase_id).first()
    if not clase:
        logger.info(f"Clase no encontrada id: {input.clase_id}")
        raise HTTPException(status_code=404, detail="Clase no encontrado")
    
    if clase.curso.docente_id != docente_id:
        logger.info(f"Docente : {docente_id} no dicta el curso {clase.curso.id}")
        raise HTTPException(status_code=404, detail="Docente no dicta el curso")
    

    new_evaluacion = Evaluacion(
        clase_id=input.clase_id,
        titulo=input.titulo,
        descripcion=input.descripcion,
        fecha=input.fecha,
        docente_id=docente_id
    )
    db.add(new_evaluacion)
    db.commit()
    db.refresh(new_evaluacion)
    logger.info(f"Evaluacion creada correctamente id: {new_evaluacion.id} titulo: {new_evaluacion.titulo}")
    return new_evaluacion


def delete_evaluacion(db:Session, evaluacion_id: int):
    db_evaluacion = db.query(Evaluacion).filter(Evaluacion.id == evaluacion_id).first()
    if db_evaluacion:
        db.delete(db_evaluacion)
        db.commit()
        logger.info(f"Evaluacion eliminado correctamente id: {evaluacion_id}")
    else:
        logger.info(f"Evaluacion no encontrado id: {evaluacion_id}")
        raise HTTPException(status_code=404, detail="Evaluacion no encontrado")
    return ApiReponseSchema(
        status_code=200,
        success=True,
        mensaje="Evaluacion eliminado correctamente"
    )


def get_resultados(db:Session, evaluacion_id: int) -> list[ResultadoEvaluacionResponse]:
    logger.info(f"Consulta resultados de evaluacion id: {evaluacion_id}")
    return db.query(ResultadoEvaluacion).filter(ResultadoEvaluacion.evaluacion_id == evaluacion_id).all()

def create_resultado(db:Session, input: ResultadoEvaluacionCreate) -> ResultadoEvaluacion:
    evaluacion = db.query(Evaluacion).filter(Evaluacion.id == input.evaluacion_id).first()
    if not evaluacion:
        logger.info(f"Evaluacion no encontrada id: {input.evaluacion_id}")
        raise HTTPException(status_code=404, detail="Evaluacion no encontrado")
    new_resultado = ResultadoEvaluacion(
        evaluacion_id=input.evaluacion_id,
        matricula_id=input.matricula_id,
        nota=input.nota,
        observaciones=input.observaciones
    )
    db.add(new_resultado)
    db.commit()
    db.refresh(new_resultado)
    logger.info(f"Resultado creado correctamente id: {new_resultado.id} nota: {new_resultado.nota}")
    return new_resultado

def delete_resultado(db:Session, resultado_id: int):
    db_resultado = db.query(ResultadoEvaluacion).filter(ResultadoEvaluacion.id == resultado_id).first()
    if db_resultado:
        db.delete(db_resultado)
        db.commit()
        logger.info(f"Resultado eliminado correctamente id: {resultado_id}")
    else:
        logger.info(f"Resultado no encontrado id: {resultado_id}")
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    return ApiReponseSchema(
        status_code=200,
        success=True,
        mensaje="Resultado eliminado correctamente"
    )
