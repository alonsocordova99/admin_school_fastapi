from admin_school_fastapi.app.db.models.rol_model import Rol
from admin_school_fastapi.app.schemas.roles_schema import RoleCreate
from fastapi import HTTPException
from sqlalchemy.orm import Session
from admin_school_fastapi.app.schemas import ApiReponseSchema
from admin_school_fastapi.app.schemas.roles_schema import RoleWithUsers
from admin_school_fastapi.app.core.utils.logging_config import logger

def get_roles(db:Session, skip: int = 0, limit: int = 10):
    logger.info(f"Consulta roles skip: {skip} limit: {limit}")
    db_roles = db.query(Rol).offset(skip).limit(limit).all()
    datos = []
    for role in db_roles:
        datos.append({
            "id": role.id,
            "nombre": role.nombre,
            "descripcion": role.descripcion,
            "num_usuarios": len(role.usuarios)
        })
    logger.info(f"Roles consultados correctamente")
    return datos
    
def get_role(db:Session, role_id: int) -> RoleWithUsers:
    db_role = db.query(Rol).filter(Rol.id == role_id).first()
    if not db_role:
        logger.info(f"Rol no encontrado id: {role_id}")
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return {
        "id": db_role.id,
        "nombre": db_role.nombre,
        "descripcion": db_role.descripcion,
        "usuarios": db_role.usuarios
    }

def create_role(db:Session, role: RoleCreate):
    new_role = Rol(
        nombre=role.nombre,
        descripcion=role.descripcion
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    logger.info(f"Role creado correctamente id: {new_role.id} nombre: {new_role.nombre}")
    return new_role

def delete_role(db:Session, role_id: int):
    db_role = db.query(Rol).filter(Rol.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
        logger.info(f"Rol eliminado correctamente id: {role_id}")
    else:
        logger.info(f"Rol no encontrado id: {role_id}")
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return ApiReponseSchema(
        status_code=200,
        success=True,
        mensaje="Rol eliminado correctamente"
    )
