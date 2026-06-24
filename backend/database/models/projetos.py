from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.professor import Professor

class Projetos(Base):
    __tablename__ = "projetos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    professor_id: Mapped[int] = mapped_column(Integer, ForeignKey("professor.id"), nullable=True)
    estudante_id: Mapped[int] = mapped_column(Integer, ForeignKey("estudante.id"), nullable=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    cronogramas: Mapped[dict] = mapped_column(JSON, nullable=True)

    estudante: Mapped[Optional["Estudante"]] = relationship("Estudante", back_populates="projetos")
    professor: Mapped[Optional["Professor"]] = relationship("Professor", back_populates="projetos")