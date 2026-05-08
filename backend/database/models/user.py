from sqlalchemy import Column, Integer, String

from backend.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=True)
    role = Column(String, nullable=False, default="aluno")