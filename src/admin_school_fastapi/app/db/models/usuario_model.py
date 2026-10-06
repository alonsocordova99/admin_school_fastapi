from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base
import enum

class RoleEnum(int, enum.Enum):
    ADMIN = 1
    DIRECTOR = 2
    DOCENTE = 3
    ESTUDIANTE = 4

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    rol_id = Column(Integer, ForeignKey("roles.id"))
    rol = relationship("Rol", back_populates="usuarios")

    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=True)
    estudiante = relationship(
        "Estudiante", 
        back_populates="usuarios"
    )

    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=True)
    docente = relationship(
        "Docente", 
        back_populates="usuarios"
    )

    def is_admin(self):
        return self.rol_id == RoleEnum.ADMIN
    
    def is_director(self):
        return self.rol_id == RoleEnum.DIRECTOR

    def is_docente(self):
        return self.rol_id == RoleEnum.DOCENTE

    def is_estudiante(self):
        return self.rol_id == RoleEnum.ESTUDIANTE
