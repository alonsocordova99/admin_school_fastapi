from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class ResultadoEvaluacion(Base):
    __tablename__ = "resultados_eval"

    id = Column(Integer, primary_key=True, index=True)
    evaluacion_id = Column(Integer, ForeignKey("evaluaciones.id"))
    matricula_id = Column(Integer, ForeignKey("matriculas.id"))
    nota = Column(Float)
    observaciones = Column(String(100), nullable=True)

    evaluacion = relationship("Evaluacion", back_populates="resultados")
