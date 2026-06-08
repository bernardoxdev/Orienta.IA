from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    telegram_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String, nullable=False, default="user")

    estudantes = relationship("Estudante", back_populates="user")
    professores = relationship("Professor", back_populates="user")