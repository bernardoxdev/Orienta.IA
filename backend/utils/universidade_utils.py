from typing import List, Optional

from backend.database.connection import SessionLocal

from backend.database.models.universidade import Universidade

async def get_universidade_by_nome_ou_sigla(texto: str) -> Optional[Universidade]:
    db = SessionLocal()

    try:
        universidade = (
            db.query(Universidade)
            .filter(
                (Universidade.nome.ilike(texto)) |
                (Universidade.sigla.ilike(texto))
            )
            .first()
        )

        return universidade
    finally:
        db.close()

async def get_universidades() -> List[Universidade]:
    db = SessionLocal()

    try:
        universidades = db.query(Universidade).all()
        return universidades
    finally:
        db.close()

if __name__ == '__main__':
    pass