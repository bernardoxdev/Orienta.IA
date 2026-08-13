from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from backend.core.jwt import SECRET_KEY, ALGORITHM
from backend.database.connection import get_db
from backend.database.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={}
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Token inválido")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user

def require_role(*roles: str):
    def checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente"
            )
        return user

    return checker

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

if __name__ == '__main__':
    pass