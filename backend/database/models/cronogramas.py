from typing import TYPE_CHECKING

from datetime import date
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.projetos import Projetos

class StatusCronograma(str, Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    CONCLUIDO = "CONCLUIDO"
    ATRASADO = "ATRASADO"

class Cronograma(Base):
    __tablename__ = "cronograma"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    projeto_id: Mapped[int] = mapped_column(Integer, ForeignKey("projetos.id", ondelete="CASCADE"), nullable=False)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=True)
    inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fim: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[StatusCronograma] = mapped_column(SqlEnum(StatusCronograma), default=StatusCronograma.PENDENTE, nullable=False)

    projeto: Mapped["Projetos"] = relationship("Projetos", back_populates="cronogramas")