from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from admin_school_fastapi.app.services import auth_services as auth_service
from admin_school_fastapi.app.schemas.user_schema import (
    UserLogin,
    UserCreate, 
    EstudianteSchemaRegister, 
    DocenteSchemaRegister, 
    UserResponse,
    EstudianteSchemaReponse,
    DocenteSchemaReponse
)
from admin_school_fastapi.app.core.utils.security import get_current_user
from admin_school_fastapi.app.schemas.auth_schema import TokenResponse
from admin_school_fastapi.app.db.models.usuario_model import RoleEnum
from admin_school_fastapi.app.core.utils.logging_config import logger
from admin_school_fastapi.app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Autenticación"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    logger.info(f"Usuario {form_data.username} intenta ingresar")
    return auth_service.login_user(
        db=db,
        user=UserLogin(email=form_data.username, password=form_data.password)
    )
    
@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    logger.info(f"Usuario {token} intenta cerrar sesion")
    return {"message": "Logout correcto"}


@router.post("/register_directy", response_model=UserResponse)
def registrar_administrador(user: UserCreate, db = Depends(get_db)):
    logger.info(f"Se intenta registrar usuario {user.email} como director")
    return auth_service.register_user(db, user, RoleEnum.DIRECTOR)
   
@router.post("/register_estudiante", response_model=EstudianteSchemaReponse)
def registrar_estudiante(userSchema: EstudianteSchemaRegister, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} registra estudiante")
    if not usuario.is_admin():
        logger.info(f"Usuario {usuario.email} no tiene permiso para crear estudiantes - Solo Admin")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return auth_service.register_estudiante_service(db, input=userSchema)

@router.post("/register_docente", response_model=DocenteSchemaReponse)
def registrar_docente(user: DocenteSchemaRegister, usuario = Depends(get_current_user), db = Depends(get_db)):
    logger.info(f"Usuario {usuario.email} registra docente")
    if not usuario.is_admin():
        logger.info(f"Usuario {usuario.email} no tiene permiso para crear docentes - Solo Admin")
        raise HTTPException(status_code=400, detail="Rol no permitido")
    return auth_service.register_docente_service(db, input=user) 
