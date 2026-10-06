from fastapi import APIRouter, Depends, HTTPException
from typing import List
from admin_school_fastapi.app.schemas.roles_schema import RoleCreate, RoleOut, RoleWithUsers
from admin_school_fastapi.app.services import roles_services as crud_role
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleOut)
def create_role(role: RoleCreate, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} crea rol")
    
    if not usuario.is_admin():
        logger.info(f"Usuario {usuario.email} no tiene permiso para crear roles - Solo Admin")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    return crud_role.create_role(db, role)

@router.get("/", response_model=List[RoleOut])
def list_roles(skip: int = 0, limit: int = 10, current_user = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {current_user.email} consulta roles")
    
    return crud_role.get_roles(db, skip, limit)

@router.delete("/{role_id}")
def delete_role(role_id: int, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} elimina rol id: {role_id}")
    
    if not usuario.is_admin():
        logger.info(f"Usuario {usuario.email} no tiene permiso para eliminar roles - Solo Admin")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    
    db_role = crud_role.delete_role(db, role_id)
    return db_role

@router.get("/{role_id}", response_model=RoleWithUsers)
def get_role(role_id: int, current_user = Depends(get_current_user), db = Depends(get_db)):
    
    logger.info(f"Usuario {current_user.email} consulta rol id: {role_id}")
    return crud_role.get_role(db, role_id)
