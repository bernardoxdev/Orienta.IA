from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base

class Horarios(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    estudante_id = Column(Integer, ForeignKey("estudante.id"), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidade.id"), nullable=False)
    matricula = Column(String, nullable=False)

    estudante = relationship("Estudante", back_populates="horarios")
    universidade = relationship("Universidade", back_populates="horarios")