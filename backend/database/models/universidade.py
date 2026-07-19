from typing import TYPE_CHECKING, Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.professor import Professor
    from backend.database.models.horarios import Horarios
    from backend.database.models.solicitacoes_vincular import SolicitacaoVincular

class Universidade(Base):
    __tablename__ = "universidade"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    sigla: Mapped[str] = mapped_column(String, nullable=False)
    cidade: Mapped[str] = mapped_column(String, nullable=False)
    estado: Mapped[str] = mapped_column(String, nullable=False)

    estudantes: Mapped[list["Estudante"]] = relationship("Estudante", back_populates="universidade")
    professores: Mapped[list["Professor"]] = relationship("Professor", back_populates="universidade")
    horarios: Mapped[list["Horarios"]] = relationship("Horarios", back_populates="universidade")
    solicitacao: Mapped["SolicitacaoVincular"] = relationship("SolicitacaoVincular", back_populates="universidade")