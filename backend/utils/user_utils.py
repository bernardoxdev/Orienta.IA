from backend.database.connection import SessionLocal
from backend.database.models.user import User

def get_user_by_email(email: str) -> User:
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == email).first()
        return user
    finally:
        db.close()

def get_user_by_telegram_id(telegram_id: str) -> User:
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        return user
    finally:
        db.close()

def criar_usario(nome: str, email: str) -> User:
    db = SessionLocal()

    try:
        user = User(
            nome=nome,
            email=email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

def atualizar_usuario_telegram_id(user: User, telegram_id: str) -> User:
    db = SessionLocal()

    try:
        user.telegram_id = telegram_id
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()

async def criar_usuario(
    telegram_id: str,
    nome: str,
    email: str,
    senha: str
) -> User:

    db = SessionLocal()

    try:
        user = User(
            telegram_id=telegram_id,
            nome=nome,
            email=email,
            senha=senha
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    finally:
        db.close()

if __name__ == '__main__':
    pass