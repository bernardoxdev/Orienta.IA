from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from brutils import is_valid_email
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.database.connection import get_db
from backend.core.jwt import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from backend.core.security import get_current_user
from backend.core.config import REFRESH_TOKEN_EXPIRE_DAYS
from backend.database.models.user import User
from backend.database.models.refresh_token import RefreshToken
from backend.database.models.schemas import LoginRequest, RegisterRequest, ChangePasswordRequest, RefreshRequest
from backend.database.models.return_schemas import LoginAndRegister, Status, Refresh

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post(
    "/login", status_code=status.HTTP_201_CREATED,
    response_model=LoginAndRegister,
    summary="Login do usuário",
    description="Realiza o login do usuário e retorna os tokens de acesso e refresh"
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    dado = data.dadoLogin.strip()

    if is_valid_email(dado):
        user = db.query(User).filter(User.email == dado).first()
    else:
        user = db.query(User).filter(User.nome == dado).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    if not pwd_context.verify(data.password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    payload = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token({"sub": str(user.id)})

    try:
        db.add(RefreshToken(token=refresh_token, user_id=user.id, expires_at=datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro ao gerar tokens")

    return LoginAndRegister(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

@router.post(
    "/refresh", status_code=status.HTTP_200_OK,
    response_model=Refresh,
    summary="Refresh do token de acesso",
    description="Gera um novo token de acesso usando o refresh token fornecido"
)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    refresh_token = data.refresh_token

    token_db = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if not token_db:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido"
        )

    if token_db.expires_at < datetime.now(timezone.utc):
        db.delete(token_db)
        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Refresh token expirado"
        )

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(401)

        user_id = payload.get("sub")

    except JWTError:

        db.delete(token_db)
        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(401, "Usuário não encontrado")

    db.delete(token_db)

    new_access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    new_refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    db.add(
        RefreshToken(
            token=new_refresh_token,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=7)
        )
    )

    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post(
    "/register", status_code=status.HTTP_201_CREATED,
    response_model=LoginAndRegister,
    summary="Registrar novo usuário",
    description="Registra um novo usuário como aluno"
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.nome == data.username).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário ou email já cadastrado"
        )
        
    if not is_valid_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email inválido"
        )
        
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário ou email já cadastrado"
        )

    user = User(
        nome=data.nome,
        username=data.username,
        email=data.email,
        senha=pwd_context.hash(data.password),
        role="usuario",
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro ao criar usuário")

    payload = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token({"sub": str(user.id)})

    try:
        db.add(RefreshToken(token=refresh_token, user_id=user.id))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro ao gerar tokens")

    return LoginAndRegister(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
    
@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    response_model=Status
)
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not pwd_context.verify(data.current_password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha atual incorreta"
        )

    user.senha = pwd_context.hash(data.new_password)

    db.commit()

    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()

    return Status(status="senha atualizada")

@router.post(
    "/logout", status_code=status.HTTP_200_OK,
    response_model=Status,
    summary="Logout do usuário",
    description="Realiza o logout do usuário, invalidando o refresh token fornecido"
)
def logout(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    token = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if token:
        db.delete(token)
        db.commit()

    return Status(status="Logout realizado")

if __name__ == '__main__':
    pass