from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id = Column(Integer, primary_key=True, index=True)
    clase_id = Column(Integer, ForeignKey("clases.id"))
    titulo = Column(String, nullable=False)
    descripcion = Column(Text)
    fecha = Column(Date)
    docente_id = Column(Integer, ForeignKey("docentes.id"))

    clase = relationship("Clase", back_populates="evaluaciones")
    resultados = relationship("ResultadoEvaluacion", back_populates="evaluacion")
    docente = relationship("Docente", backref="evaluaciones")
