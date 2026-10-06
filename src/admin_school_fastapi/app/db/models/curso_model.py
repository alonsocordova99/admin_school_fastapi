from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    grado = Column(String(50), nullable=False)
    seccion = Column(String(10), nullable=False)

    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=True)
    periodo_id = Column(Integer, ForeignKey("periodos.id"))
    
    docente = relationship("Docente", back_populates="cursos")
    periodo = relationship("Periodo", back_populates="cursos")

    matriculas = relationship("Matricula", back_populates="curso")
    clases = relationship("Clase", back_populates="curso")




