from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import  relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.horarios import Horarios
    from backend.database.models.projetos import Projetos
    from backend.database.models.user import User
    from backend.database.models.universidade import Universidade
    from backend.database.models.solicitacoes_vincular import SolicitacaoVincular

class Estudante(Base):
    __tablename__ = "estudante"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    universidade_id: Mapped[int] = mapped_column(Integer, ForeignKey("universidade.id"), nullable=False)
    matricula: Mapped[str] = mapped_column(String, nullable=False)
    curso: Mapped[str] = mapped_column(String, nullable=True)
    periodo: Mapped[int] = mapped_column(Integer, nullable=True)
    lattes: Mapped[str] = mapped_column(String, nullable=True)
    previsao_conclusao: Mapped[str] = mapped_column(String, nullable=True)

    horarios: Mapped[list["Horarios"]] = relationship("Horarios", back_populates="estudante")
    projetos: Mapped["Projetos"] = relationship("Projetos", back_populates="estudante")

    user: Mapped["User"] = relationship("User", back_populates="estudantes")
    universidade: Mapped["Universidade"] = relationship("Universidade", back_populates="estudantes")
    solicitacao: Mapped["SolicitacaoVincular"] = relationship("SolicitacaoVincular", back_populates="estudante")