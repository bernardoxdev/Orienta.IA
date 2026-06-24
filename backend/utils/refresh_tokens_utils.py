from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.database.models.refresh_token import RefreshToken

def clear_expired_tokens(db: Session):
    db.query(RefreshToken).filter(RefreshToken.expires_at < datetime.now(timezone.utc)).delete()

    db.commit()

if __name__ == '__main__':
    pass