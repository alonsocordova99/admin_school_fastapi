from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    nro_documento = Column(String(100), nullable=False)
    nombre_apoderado = Column(String(100), nullable=False)
    telefono_apoderado = Column(String(100), nullable=True)
    
    usuarios = relationship("Usuario", back_populates="estudiante")
    matriculas = relationship("Matricula", back_populates="estudiante")

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"
