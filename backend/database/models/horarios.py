from sqlalchemy import Column, Integer, String, ForeignKey

from backend.database.base import Base

class Horarios(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    estudante_id = Column(Integer, ForeignKey("estudante.id"), nullable=False)
    universidade_id = Column(Integer, ForeignKey("universidade.id"), nullable=False)
    matricula = Column(String, nullable=False)
