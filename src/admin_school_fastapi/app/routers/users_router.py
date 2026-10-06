from fastapi import APIRouter, Depends, HTTPException
from admin_school_fastapi.app.schemas.user_schema import  UserResponse
from admin_school_fastapi.app.services import users_services as crud_user
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.db.models.usuario_model import Usuario
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/me")
def read_users_me(current_user: Usuario = Depends(get_current_user)):
    logger.info(f"Usuario {current_user.email} solicita su informacion")
    return {
        "id": current_user.id, 
        "email": current_user.email,
        "rol": current_user.rol_id
    }

@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    if not current_user.is_admin():
        logger.info(f"Usuario {current_user.email} no tiene permiso para consultar usuarios")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    logger.info(f"Usuario {current_user.email} consulta usuarios")
    return crud_user.get_users(db, skip=skip, limit=limit)



@router.delete("/{user_id}")
def delete_user(user_id: int, current_user = Depends(get_current_user)):
    if not current_user.is_admin():
        logger.info(f"Usuario {current_user.email} no tiene permiso para eliminar usuarios")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    logger.info(f"Usuario {current_user.email} elimina usuario id: {user_id}")
    db_user = crud_user.delete_user(user_id=user_id)
    return db_user