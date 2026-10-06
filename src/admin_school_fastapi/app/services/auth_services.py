from admin_school_fastapi.app.schemas.user_schema import UserLogin
from admin_school_fastapi.app.core.utils.security import create_access_token
from admin_school_fastapi.app.core.utils.hashing import verify_password, get_password_hash
from admin_school_fastapi.app.db.models.usuario_model import Usuario, RoleEnum
from admin_school_fastapi.app.db.models.estudiante_model import Estudiante
from admin_school_fastapi.app.db.models.docente_model import Docente
from fastapi import HTTPException
from admin_school_fastapi.app.schemas.user_schema import (
    UserCreate, 
    EstudianteSchemaRegister, 
    DocenteSchemaRegister,
    EstudianteSchemaReponse,
    DocenteSchemaReponse
)
from admin_school_fastapi.app.schemas.auth_schema import TokenResponse
from admin_school_fastapi.app.core.utils.logging_config import logger
from sqlalchemy.orm import Session

def login_user(db: Session, user: UserLogin):

    userModel = db.query(Usuario).filter(Usuario.email == user.email).first()
    if not userModel or not verify_password( user.password, userModel.password_hash):
        logger.info(f"Error al intentar ingresar al sistema: Credenciales incorrectas")
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    logger.info(f"Usuario ingresado correctamente - Rol: {userModel.rol_id}")
    access_token = create_access_token(user = userModel)
    logger.info(f"Token de acceso creado correctamente")
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

def register_user(db:Session,input: UserCreate, rol_id:int)-> Usuario:
    logger.info(f"Se intenta registrar usuario {input.email} con rol {rol_id}")
    new_user = Usuario(
        nombre=input.nombre,
        email=input.email,
        rol_id=rol_id
    )
    hashed_password = get_password_hash(input.password)
    new_user.password_hash = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Usuario creado correctamente id: {new_user.id} nombre: {new_user.nombre}")
    return new_user


def register_estudiante_service(db:Session, input: EstudianteSchemaRegister) -> EstudianteSchemaReponse:

    logger.info(f"Se intenta registrar estudiante {input.email}")
    estudiante = Estudiante(
        nombres=input.nombres,
        apellidos=input.apellidos,
        nro_documento=input.nro_documento,
        nombre_apoderado=input.nombre_apoderado,
        telefono_apoderado=input.telefono_apoderado
    )
    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)
    logger.info(f"Se registra estudiante {input.email}")
    new_user = Usuario(
        nombre=input.nombres + " " + input.apellidos,
        email=input.email,
        rol_id=RoleEnum.ESTUDIANTE,
        estudiante_id=estudiante.id
    )
    hashed_password = get_password_hash(input.nro_documento)
    new_user.password_hash = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Estudiante {input.email} registrado correctamente con su usuario")
    
    return EstudianteSchemaReponse(
        status_code=200,
        success=True,
        mensaje="Estudiante creado correctamente",
        user_id=new_user.id,
        estudiante_id=estudiante.id,
        username=new_user.email,
        password=input.nro_documento
    )

def register_docente_service(db:Session, input: DocenteSchemaRegister) -> DocenteSchemaReponse:
    logger.info(f"Se intenta registrar docente {input.email}")
    docente = Docente(
        nombre= input.nombres,
        apellido= input.apellidos,
        especialidad= input.especialidad,
        nro_documento= input.nro_documento,
        telefono= input.telefono
    )
    db.add(docente)
    db.commit()
    db.refresh(docente)
    logger.info(f"Se registra docente {input.email}")
    new_user = Usuario(
        nombre=input.nombres + " " + input.apellidos,
        email=input.email,
        rol_id=RoleEnum.DOCENTE,
        docente_id=docente.id
    )
    hashed_password = get_password_hash(input.nro_documento)
    new_user.password_hash = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"Docente {input.email} registrado correctamente con su usuario")
    return DocenteSchemaReponse(
        status_code=200,
        success=True,
        mensaje="Docente creado correctamente",
        user_id=new_user.id,
        docente_id=docente.id,
        username=new_user.email,
        password=input.nro_documento
    )
        
    