from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    rol_id: int
    docente_id: Optional[int] = None
    estudiante_id: Optional[int] = None
    class Config:
        from_attributes = True



class EstudianteSchemaRegister(BaseModel):
    nombres: str
    apellidos: str
    nro_documento: str
    email: str
    nombre_apoderado: Optional[str] = None
    telefono_apoderado: Optional[str] = None

class EstudianteSchemaReponse(BaseModel):
    status_code: int
    success: bool
    mensaje: str
    user_id: int
    estudiante_id: int
    username: str
    password: str

class DocenteSchemaRegister(BaseModel):
    nombres: str
    apellidos: str
    telefono: str
    especialidad: str
    email: str
    nro_documento: str

class DocenteSchemaReponse(BaseModel):
    status_code: int
    success: bool
    mensaje: str
    user_id: int
    docente_id: int
    username: str
    password: str