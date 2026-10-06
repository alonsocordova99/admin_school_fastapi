from admin_school_fastapi.app.db.models.usuario_model import Usuario
from fastapi import HTTPException
from sqlalchemy.orm import Session
from admin_school_fastapi.app.schemas import ApiReponseSchema
from admin_school_fastapi.app.core.utils.logging_config import logger

def get_users(db:Session, skip: int = 0, limit: int = 10):
    logger.info(f"Consulta usuarios skip: {skip} limit: {limit}")
    usuarios_db = db.query(Usuario).offset(skip).limit(limit).all()
    datos = []
    for usuario in usuarios_db:
        datos.append({
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "rol_id": usuario.rol_id,
            "docente_id": usuario.docente_id,
            "estudiante_id": usuario.estudiante_id
        })
    return datos

def get_user(db:Session, user_id: int):
    logger.info(f"Consulta usuario id: {user_id}")
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def delete_user(db:Session, user_id: int):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not db_user:
        logger.info(f"Usuario no encontrado id: {user_id}")
        raise HTTPException(status_code=404, detail="User no encontrado")
        
    db.delete(db_user)
    db.commit()
    logger.info(f"Usuario eliminado correctamente id: {user_id}")
    
    return ApiReponseSchema(
        status_code=200,
        success=True,
        mensaje="User eliminado correctamente"
    )