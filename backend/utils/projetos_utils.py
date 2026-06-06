from typing import List

from backend.database.connection import SessionLocal
from backend.database.models.projetos import Projetos

async def get_projetos() -> List[Projetos]:
    db = SessionLocal()

    try:
        projetos = db.query(Projetos).all()
        return projetos
    finally:
        db.close()

if __name__ == '__main__':
    pass