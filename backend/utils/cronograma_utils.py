from datetime import date

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models.cronogramas import Cronograma, StatusCronograma

def create_cronograma(projeto_id: int, titulo: str, descricao: str, inicio: date, fim: date, status: StatusCronograma) -> Cronograma:
    db: Session = SessionLocal()

    try:
        cronograma: Cronograma = Cronograma(
            projeto_id=projeto_id,
            titulo=titulo,
            descricao=descricao,
            inicio=inicio,
            fim=fim,
            status=status
        )

        db.add(cronograma)
        db.commit()
        db.refresh(cronograma)

        return cronograma

    finally:
        db.close()

def get_cronogramas_projeto(projeto_id: int) -> list[type[Cronograma]]:
    db: Session = SessionLocal()

    try:
        cronogramas = db.query(Cronograma).filter(Cronograma.projeto_id==projeto_id).all()

        return cronogramas

    finally:
        db.close()

if __name__ == '__main__':
    pass