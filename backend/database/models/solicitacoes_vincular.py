from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.user import User
    from backend.database.models.universidade import Universidade

class SolicitacaoVincular(Base):
    __tablename__ = "solicitacoes_vincular"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String, nullable=False)
    universidade_id: Mapped[int] = mapped_column(Integer, ForeignKey("universidade.id"), nullable=False)
    departamento: Mapped[str] = mapped_column(String, nullable=True)
    matricula: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="solicitacao")
    universidade: Mapped["Universidade"] = relationship("Universidade", back_populates="solicitacao")