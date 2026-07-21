from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.projetos import Projetos
    from backend.database.models.user import User
    from backend.database.models.universidade import Universidade

class Professor(Base):
    __tablename__ = "professor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    universidade_id: Mapped[int] = mapped_column(Integer, ForeignKey("universidade.id"), nullable=False)
    departamento: Mapped[str] = mapped_column(String, nullable=False)
    lattes: Mapped[str] = mapped_column(String, nullable=True)
    area_pesquisa: Mapped[str] = mapped_column(String, nullable=True)
    sala: Mapped[str] = mapped_column(String, nullable=True)

    projetos: Mapped[list["Projetos"]] = relationship("Projetos", back_populates="professor")

    user: Mapped["User"] = relationship("User", back_populates="professores")
    universidade: Mapped["Universidade"] = relationship("Universidade", back_populates="professores")