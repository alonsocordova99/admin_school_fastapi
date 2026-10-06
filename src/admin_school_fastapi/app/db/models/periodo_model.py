from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Periodo(Base):
    __tablename__ = "periodos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)

    cursos = relationship("Curso", back_populates="periodo")
