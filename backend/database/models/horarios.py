from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.database.base import Base

if TYPE_CHECKING:
    from backend.database.models.estudante import Estudante
    from backend.database.models.universidade import Universidade

class Horarios(Base):
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estudante_id: Mapped[int] = mapped_column(Integer, ForeignKey("estudante.id"), nullable=False)
    universidade_id: Mapped[int] = mapped_column(Integer, ForeignKey("universidade.id"), nullable=False)
    matricula: Mapped[str] = mapped_column(String, nullable=False)

    estudante: Mapped["Estudante"] = relationship("Estudante", back_populates="horarios")
    universidade: Mapped["Universidade"] = relationship("Universidade", back_populates="horarios")