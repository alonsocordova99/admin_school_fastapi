from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from admin_school_fastapi.app.db.base import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(Text)

    usuarios = relationship("Usuario", back_populates="rol")