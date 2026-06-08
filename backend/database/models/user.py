from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.professor import Professor

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    telegram_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")

    estudantes: Mapped["Estudante"] = relationship("Estudante", back_populates="user")
    professores: Mapped["Professor"] = relationship("Professor", back_populates="user")