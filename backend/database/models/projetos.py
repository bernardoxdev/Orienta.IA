from sqlalchemy import Column, Integer, String, ForeignKey, JSON

from backend.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    professor_id = Column(Integer, ForeignKey("professor.id"), nullable=True)
    estudante_id = Column(Integer, ForeignKey("estudante.id"), nullable=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    cronogramas = Column(JSON, nullable=True)