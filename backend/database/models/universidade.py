from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database.base import Base

class Universidade(Base):
    __tablename__ = "universidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    sigla = Column(String, nullable=False)

    estudantes = relationship("Estudante", back_populates="universidade")
    professores = relationship("Professor", back_populates="universidade")