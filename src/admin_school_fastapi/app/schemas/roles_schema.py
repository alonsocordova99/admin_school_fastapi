from pydantic import BaseModel
from typing import List

class RoleBase(BaseModel):
    nombre: str
    descripcion: str | None = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int
    num_usuarios: int = 0
    class Config:
        from_attributes = True



## para el detalle
class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

class RoleWithUsers(RoleBase):
    id: int
    usuarios: List[UsuarioSchema] = []
    class Config:
        from_attributes = True


