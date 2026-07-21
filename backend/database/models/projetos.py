from typing import TYPE_CHECKING, Optional

from datetime import date
from enum import Enum

from sqlalchemy import Integer, String, ForeignKey, JSON, Date, Enum as SQLEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.professor import Professor
    from backend.database.models.cronogramas import Cronograma

class ContextoOrientacao(str, Enum):
    IC = "IC"
    TCC = "TCC"
    MESTRADO = "MESTRADO"
    DOUTORADO = "DOUTORADO"
    OUTRO = "OUTRO"

class Projetos(Base):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    professor_id: Mapped[int] = mapped_column(Integer, ForeignKey("professor.id"), nullable=True)
    estudante_id: Mapped[int] = mapped_column(Integer, ForeignKey("estudante.id"), nullable=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="Em andamento")
    data_inicio: Mapped[date] = mapped_column(Date, nullable=True)
    data_fim: Mapped[date] = mapped_column(Date, nullable=True)
    contexto: Mapped[ContextoOrientacao] = mapped_column(SQLEnum(ContextoOrientacao), nullable=True)
    palavras_chave: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    estudante: Mapped[Optional["Estudante"]] = relationship("Estudante", back_populates="projetos")
    professor: Mapped[Optional["Professor"]] = relationship("Professor", back_populates="projetos")
    cronogramas: Mapped[list["Cronograma"]] = relationship("Cronograma", back_populates="projeto", cascade="all, delete-orphan")