from typing import Optional

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal

from backend.database.models.user import User

async def is_user_admin_by_telegram(telegram_id) -> bool:
    db: Session = SessionLocal()

    try:
        user: Optional[User] = db.query(User).filter(User.telegram_id==telegram_id).first()

        if not user:
            return False

        if user.role != "admin":
            return False

        return True
    finally:
        db.close()

if __name__ == '__main__':
    pass