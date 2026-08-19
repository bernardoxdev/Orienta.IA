import traceback

from sqlalchemy.orm import Session

from typing import Optional

from brutils import is_valid_email

from backend.database.models.user import User
from backend.database.models.universidade import Universidade
from backend.database.models.estudante import Estudante
from backend.database.models.professor import Professor
from backend.database.models.return_schemas import UserVerification, StatusResponse

from backend.core.security import hash_password

from backend.database.connection import SessionLocal

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

async def atualizar_usuario_telegram_id(user: User, telegram_id: str) -> User:
    db = SessionLocal()

    try:
        user.telegram_id = telegram_id

        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()

async def criar_usuario(telegram_id: str, username: str, nome: str, email: str, senha: str) -> User:
    db = SessionLocal()

    try:
        user = User(
            telegram_id=telegram_id,
            username=username,
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

async def get_role_user_telegram_id(telegram_id: str) -> str:
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()

        return user.role if user else None
    finally:
        db.close()

async def exists_user_telegram(telegram_id: str) -> bool:
    db = SessionLocal()

    try:
        return db.query(User).filter(User.telegram_id == telegram_id).first() is not None
    finally:
        db.close()
        
def validar_criar__user(user_verification: UserVerification) -> StatusResponse:
    db: Session = SessionLocal()

    try:
        if not is_valid_email(user_verification.email):
            return StatusResponse(
                success=False,
                status="E-mail informado não é válido."
            )

        if not user_verification.username.strip():
            return StatusResponse(
                success=False,
                status="Username não pode ser vazio."
            )

        if not user_verification.nome.strip():
            return StatusResponse(
                success=False,
                status="Nome não pode ser vazio."
            )

        if not user_verification.senha:
            return StatusResponse(
                success=False,
                status="Senha não pode ser vazia."
            )

        if user_verification.tipo not in ["estudante", "professor"]:
            return StatusResponse(
                success=False,
                status="Tipo de usuário inválido."
            )

        universidade = db.query(Universidade).filter(Universidade.id == user_verification.universidade_id).first()

        if not universidade:
            return StatusResponse(
                success=False,
                status="Universidade não encontrada."
            )

        email_existente = db.query(User).filter(User.email == user_verification.email).first()

        if email_existente:
            return StatusResponse(
                success=False,
                status="E-mail já está cadastrado."
            )

        username_existente = db.query(User).filter(User.username == user_verification.username).first()

        if username_existente:
            return StatusResponse(
                success=False,
                status="Username já está cadastrado."
            )

        if user_verification.telegram_id:
            telegram_existente = db.query(User).filter(User.telegram_id == user_verification.telegram_id).first()

            if telegram_existente:
                return StatusResponse(
                    success=False,
                    status="Telegram ID já está vinculado a outro usuário."
                )

        if user_verification.tipo == "estudante":

            if not user_verification.matricula:
                return StatusResponse(
                    success=False,
                    status="Matrícula é obrigatória para estudantes."
                )

            if not user_verification.curso:
                return StatusResponse(
                    success=False,
                    status="Curso é obrigatório para estudantes."
                )

        elif user_verification.tipo == "professor":

            if not user_verification.departamento:
                return StatusResponse(
                    success=False,
                    status="Departamento é obrigatório para professores."
                )

        senha_hash = hash_password(user_verification.senha)

        user = User(
            telegram_id=user_verification.telegram_id,
            nome=user_verification.nome,
            username=user_verification.username,
            email=user_verification.email,
            senha=senha_hash,
            role=user_verification.role,
            ativo=True
        )

        db.add(user)
        db.flush()

        if user_verification.tipo == "estudante":
            estudante = Estudante(
                user_id=user.id,
                universidade_id=user_verification.universidade_id,
                matricula=user_verification.matricula,
                curso=user_verification.curso,
                periodo=user_verification.periodo,
                lattes=user_verification.lattes,
                previsao_conclusao=user_verification.previsao_conclusao
            )

            db.add(estudante)

        elif user_verification.tipo == "professor":
            professor = Professor(
                user_id=user.id,
                universidade_id=user_verification.universidade_id,
                departamento=user_verification.departamento,
                lattes=user_verification.lattes,
                area_pesquisa=user_verification.area_pesquisa,
                sala=user_verification.sala
            )

            db.add(professor)

        db.commit()

        return StatusResponse(
            success=True,
            status="Usuário criado com sucesso."
        )

    except Exception as e:
        db.rollback()

        traceback.print_exc()

        return StatusResponse(
            success=False,
            status=f"Erro ao criar usuário: {e}"
        )

    finally:
        db.close()
        
def desativar_user_by_id(usuario_id: int) -> StatusResponse:
    db: Session = SessionLocal()
    
    try:
        user = db.query(User).filter(User.id == usuario_id).first()
        
        if not user:
            return StatusResponse(
                success=False,
                status="Usuário não encontrado"
            )

        user.ativo = False
        
        db.commit()
        db.refresh(user)
        
        return StatusResponse(
            success=True,
            status=f"Usuário desativado com sucesso: {usuario_id}"
        )
        
    except Exception as e:
        db.rollback()
        return StatusResponse(
            success=False,
           status=f"Erro ao desativar user: {usuario_id}" 
        )
    
    finally:
        db.close()

def atualizar_user(user_verification: UserVerification) -> Optional[UserVerification]:
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_verification.id).first()
        
        if not user:
            return None

        user.nome = user_verification.nome
        user.username = user_verification.username
        user.email = user_verification.email
        user.telegram_id = user_verification.telegram_id
        user.role = user_verification.role
        user.ativo = user_verification.ativo

        if user_verification.senha:
            user.senha = hash_password(user_verification.senha)

        user.tipo = user_verification.tipo
        
        if user_verification.tipo == "estudante":
            estudante = db.query(Estudante).filter(Estudante.user_id == user.id).first()
        
            if user_verification.universidade_id:
                estudante.universidade_id = user_verification.universidade_id
            estudante.matricula = user_verification.matricula
            estudante.curso = user_verification.curso
            estudante.periodo = user_verification.periodo
            estudante.lattes = user_verification.lattes
            estudante.previsao_conclusao = user_verification.previsao_conclusao
            
            db.flush()

        elif user_verification.tipo == "professor":
            professor = db.query(Professor).filter(Professor.user_id == user.id).first()
            
            if user_verification.universidade_id:
                professor.universidade_id = user_verification.universidade_id
            professor.departamento = user_verification.departamento
            professor.area_pesquisa = user_verification.area_pesquisa
            professor.sala = user_verification.sala
            
            db.flush()

        db.commit()
        db.refresh(user)

        return UserVerification

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

if __name__ == '__main__':
    pass