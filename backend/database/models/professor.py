from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base import Base

class Professor(Base):
    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidade.id"), nullable=False)
    departamento = Column(String, nullable=False)

    projetos = relationship("Projetos", back_populates="professor")

    user = relationship("User", back_populates="professores")
    universidade = relationship("Universidade", back_populates="professores")