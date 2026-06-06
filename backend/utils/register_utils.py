from backend.database.connection import SessionLocal
from backend.database.models.estudante import Estudante
from backend.database.models.professor import Professor
from backend.utils.user_utils import get_user_by_telegram_id

register_infos = {}

async def vincular_aluno_by_telegram(telegram_id: str, universidade_id: int, matricula: str) -> bool:
    user = get_user_by_telegram_id(telegram_id)

    if user:
        db = SessionLocal()

        try:
            estudante = Estudante(
                user_id=user.id,
                matricula=matricula,
                universidade_id=universidade_id
            )
            db.add(estudante)
            db.commit()
            db.refresh(estudante)
            return True
        finally:
            db.close()

    return False

async def vincular_professor_by_telegram(telegram_id: str, universidade_id: int, departamento: str) -> bool:
    user = get_user_by_telegram_id(telegram_id)

    if user:
        db = SessionLocal()

        try:
            professor = Professor(
                user_id=user.id,
                universidade_id=universidade_id,
                departamento=departamento
            )
            db.add(professor)
            db.commit()
            db.refresh(professor)
            return True
        finally:
            db.close()

    return False

async def verificar_vinculado(telegram_id: str) -> bool:
    user = get_user_by_telegram_id(telegram_id)

    if not user:
        return False

    db = SessionLocal()

    try:
        estudante = db.query(Estudante).filter(
            Estudante.user_id == user.id
        ).first()

        if estudante:
            return True

        professor = db.query(Professor).filter(
            Professor.user_id == user.id
        ).first()

        if professor:
            return True

        return False
    finally:
        db.close()

async def realizar_login(telegram_id: str, email: str, senha: str) -> bool:
    user = get_user_by_telegram_id(telegram_id)

    if not user:
        return False

    db = SessionLocal()

    try:
        if user.email == email and user.senha == senha:
            return True
        else:
            return False
    finally:
        db.close()

if __name__ == '__main__':
    pass