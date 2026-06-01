from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import  relationship

from backend.database.base import Base

class Estudante(Base):
    __tablename__ = "estudante"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidade.id"), nullable=False)
    matricula = Column(String, nullable=False)

    horarios = relationship("Horarios", back_populates="estudante")
    projetos = relationship("Projetos", back_populates="estudante")