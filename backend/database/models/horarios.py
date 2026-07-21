from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante

class Horarios(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estudante_id: Mapped[int] = mapped_column(Integer, ForeignKey("estudante.id"), nullable=False)
    dia_semana: Mapped[str] = mapped_column(String, nullable=False)
    hora_inicio: Mapped[str] = mapped_column(String, nullable=False)
    hora_fim: Mapped[str] = mapped_column(String, nullable=False)
    modalidade: Mapped[str] = mapped_column(String, nullable=False)

    estudante: Mapped["Estudante"] = relationship("Estudante", back_populates="horarios")