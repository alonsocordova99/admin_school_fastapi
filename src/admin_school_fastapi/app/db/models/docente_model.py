from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    especialidad = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(100), nullable=False)
    nro_documento = Column(String(100), nullable=False)

    usuarios = relationship("Usuario", back_populates="docente")
    cursos = relationship("Curso", back_populates="docente")

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"