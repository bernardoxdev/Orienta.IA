from typing import Optional, List

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models.user import User
from backend.database.models.professor import Professor
from backend.database.models.estudante import Estudante
from backend.database.models.solicitacoes_vincular import SolicitacaoVincular

async def get_solicitacoes() -> List[SolicitacaoVincular]:
    db = SessionLocal()

    try:
        solicitacoes = db.query(SolicitacaoVincular).all()
        return solicitacoes

    finally:
        db.close()

async def get_solicitacao_by_telegram(telegram_id) -> Optional[SolicitacaoVincular]:
    db: Session = SessionLocal()

    try:
        user: Optional[User] = db.query(User).filter(User.telegram_id==telegram_id).first()

        if not user:
            return None

        return db.query(SolicitacaoVincular).filter(SolicitacaoVincular.user_id==user.id).first()

    finally:
        db.close()

async def has_solicitacao_by_telegram(telegram_id) -> bool:
    db: Session = SessionLocal()

    try:
        user: Optional[User] = db.query(User).filter(User.telegram_id==telegram_id).first()

        if not user:
            return False

        return db.query(SolicitacaoVincular).filter(SolicitacaoVincular.user_id==user.id).first() is not None

    finally:
        db.close()

async def gerar_solicitacao(data: dict) -> SolicitacaoVincular:
    db: Session = SessionLocal()

    try:
        solicitacao = SolicitacaoVincular(**data)

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    finally:
        db.close()

async def aceitar_solicitacao(solicitacao: SolicitacaoVincular) -> bool:
    db: Session = SessionLocal()

    try:
        dado = None

        if solicitacao.tipo == "estudante":
            dado: Optional[Estudante] = Estudante(
                user_id=solicitacao.user_id,
                matricula=solicitacao.matricula,
                universidade_id=solicitacao.universidade_id,
            )
        else:
            dado: Optional[Professor] = Professor(
                user_id=solicitacao.user_id,
                universidade_id=solicitacao.universidade_id,
                departamento=solicitacao.departamento
            )

        db.add(dado)
        db.commit()
        db.refresh(dado)

        return True

    finally:
        db.close()

if __name__ == '__main__':
    pass