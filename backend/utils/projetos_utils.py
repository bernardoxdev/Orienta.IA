from typing import List
from datetime import date

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models.projetos import Projetos, ContextoOrientacao

async def get_projetos() -> List[Projetos]:
    db = SessionLocal()

    try:
        projetos = db.query(Projetos).all()
        return projetos
    finally:
        db.close()

def create_projeto(professor_id: int, estudante_id: int, titulo: str, descricao: str, status: str, data_inicio: date, data_fim: date, contexto: ContextoOrientacao, palavras_chave: List[str]) -> Projetos:
    db: Session = SessionLocal()

    try:
        projeto: Projetos = Projetos(
            professor_id=professor_id,
            estudante_id=estudante_id,
            titulo=titulo,
            descricao=descricao,
            status=status,
            data_inicio=data_inicio,
            data_fim=data_fim,
            contexto=contexto,
            palavras_chave=palavras_chave
        )

        db.add(projeto)
        db.commit()
        db.refresh(projeto)

        return projeto

    finally:
        db.close()

if __name__ == '__main__':
    pass