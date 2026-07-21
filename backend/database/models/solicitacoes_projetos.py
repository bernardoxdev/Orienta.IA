from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.professor import Professor
    from backend.database.models.projetos import Projetos

class SolicitacaoProjeto(Base):
    __tablename__ = "solicitacoes_projetos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estudante_id: Mapped[int] = mapped_column(Integer, ForeignKey("estudante.id"), nullable=False)
    professor_id: Mapped[int] = mapped_column(Integer, ForeignKey("professor.id"), nullable=False)
    projeto_id: Mapped[int] = mapped_column(Integer, ForeignKey("projetos.id"), nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    origem: Mapped[int] = mapped_column(Integer, nullable=False) # 1 para estudante, 2 para professor

    estudante: Mapped["Estudante"] = relationship("Estudante", back_populates="solicitacao")
    professor: Mapped["Professor"] = relationship("Professor", back_populates="solicitacao")
    projeto: Mapped["Projetos"] = relationship("Projetos", back_populates="solicitacao")