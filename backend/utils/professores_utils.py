from typing import List

from backend.database.connection import SessionLocal
from backend.database.models.professor import Professor

async def get_professores() -> List[Professor]:
    db = SessionLocal()

    try:
        professores = db.query(Professor).all()
        return professores
    finally:
        db.close()

if __name__ == '__main__':
    pass