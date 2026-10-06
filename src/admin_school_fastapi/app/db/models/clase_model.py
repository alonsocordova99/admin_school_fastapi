from sqlalchemy import Column, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Clase(Base):
    __tablename__ = "clases"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    fecha_fin = Column(Date, nullable=True)
    link_meeting = Column(String, nullable=True)
    link_video = Column(String, nullable=True)

    curso_id = Column(Integer, ForeignKey("cursos.id"))
    curso = relationship("Curso", back_populates="clases")

    evaluaciones = relationship("Evaluacion", back_populates="clase")
