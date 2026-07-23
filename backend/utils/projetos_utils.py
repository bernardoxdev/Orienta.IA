from typing import List, Any, Optional

from datetime import date

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models.projetos import Projetos, ContextoOrientacao, StatusProjeto
from backend.database.models.estudante import Estudante
from backend.database.models.professor import Professor
from backend.database.models.solicitacoes_projetos import SolicitacaoCancelamento, SolicitacaoProjeto

async def get_projetos() -> List[Projetos]:
    db = SessionLocal()

    try:
        projetos = db.query(Projetos).all()
        return projetos
    finally:
        db.close()

def create_projeto(professor_id: int, estudante_id: int, titulo: str, descricao: str, status: str, data_inicio: date, data_fim: date, contexto: ContextoOrientacao, palavras_chave: List[str]) -> Projetos:
    db: Session = SessionLocal()

    try:
        projeto: Projetos = Projetos(
            professor_id=professor_id,
            estudante_id=estudante_id,
            titulo=titulo,
            descricao=descricao,
            status=status,
            data_inicio=data_inicio,
            data_fim=data_fim,
            contexto=contexto,
            palavras_chave=palavras_chave
        )

        db.add(projeto)
        db.commit()
        db.refresh(projeto)

        return projeto

    finally:
        db.close()

def get_projetos_sem_aluno() -> List[type[Projetos]]:
    db: Session = SessionLocal()

    try:
        projetos = db.query(Projetos).filter(Projetos.estudante_id==None).all()

        return projetos

    finally:
        db.close()

def get_filters(professor_id: int = None, estudante_id: int = None, finalizados: StatusProjeto = None, contexto: ContextoOrientacao = None) -> list[Any]:
    filters = []

    if professor_id is not None:
        filters.append(Projetos.professor_id==professor_id)

    if estudante_id is not None:
        filters.append(Projetos.estudante_id==estudante_id)

    if finalizados:
        filters.append(Projetos.status==finalizados)

    if contexto is not None:
        filters.append(Projetos.contexto==contexto)

    return filters

def get_projetos_por_professor(professor_id: int, finalizados: bool, contexto: ContextoOrientacao) -> List[type[Projetos]]:
    db: Session = SessionLocal()

    try:
        projetos = db.query(Projetos).filter(get_filters(professor_id, None, finalizados, contexto)).all()

        return projetos

    finally:
        db.close()

def get_projetos_por_estudante(estudante_id: int, finalizados: bool, contexto: ContextoOrientacao) -> List[type[Projetos]]:
    db: Session = SessionLocal()

    try:
        projetos = db.query(Projetos).filter(get_filters(None, estudante_id, finalizados, contexto)).all()

        return projetos

    finally:
        db.close()

async def solicitar_cancelamento_projeto(projeto_id: int, estudante_id: int, professor_id: int, mandante: int, explicacao: str) -> Optional[SolicitacaoCancelamento]:
    db: Session = SessionLocal()

    try:
        projeto = db.get(Projetos, projeto_id)
        estudante = db.get(Estudante, estudante_id)
        professor = db.get(Professor, professor_id)

        if projeto is None or estudante is None or professor is None:
            return None

        solicitacao = SolicitacaoCancelamento(
            estudante_id=estudante_id,
            professor_id=professor_id,
            projeto_id=projeto_id,
            descricao=explicacao,
            origem=mandante
        )

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    finally:
        db.close()

async def mudar_status_projeto(projeto_id: int, novo_status: StatusProjeto) -> Optional[Projetos]:
    db: Session = SessionLocal()

    try:
        projeto: Optional[Projetos] = db.get(Projetos, projeto_id)

        if projeto is None:
            return None

        projeto.status = novo_status

        db.commit()
        db.refresh(projeto)

        return projeto

    finally:
        db.close()

async def atualizar_descricao_projeto(projeto_id: int, nova_descricao: str) -> Optional[Projetos]:
    db: Session = SessionLocal()

    try:
        projeto: Optional[Projetos] = db.get(Projetos, projeto_id)

        if projeto is None:
            return None

        projeto.descricao = nova_descricao

        db.commit()
        db.refresh(projeto)

        return projeto

    finally:
        db.close()

async def gerar_solicitacao_projeto(estudante_id: int, projeto_id: int) -> SolicitacaoProjeto:
    db: Session = SessionLocal()

    try:
        projeto: SolicitacaoProjeto = SolicitacaoProjeto(
            estudante_id=estudante_id,
            projeto_id=projeto_id
        )

        db.add(projeto)
        db.commit()
        db.refresh(projeto)

        return projeto

    finally:
        db.close()

if __name__ == '__main__':
    pass