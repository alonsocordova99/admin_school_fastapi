from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base
import datetime

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_registro = Column(Date, default=datetime.datetime.now)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    curso_id = Column(Integer, ForeignKey("cursos.id"))

    estudiante = relationship("Estudiante", back_populates="matriculas")
    curso = relationship("Curso", back_populates="matriculas")

    @property
    def nombre_estudiante(self):
        return self.estudiante.nombre_completo
    
    @property
    def nombre_curso(self):
        return self.curso.nombre