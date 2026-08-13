from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.professor import Professor
    from backend.database.models.solicitacoes_vincular import SolicitacaoVincular

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    telegram_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    estudantes: Mapped["Estudante | None"] = relationship("Estudante", back_populates="user")
    professores: Mapped["Professor | None"] = relationship("Professor", back_populates="user")
    solicitacao: Mapped["SolicitacaoVincular"] = relationship("SolicitacaoVincular", back_populates="user")