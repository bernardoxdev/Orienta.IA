from typing import List, Any

from datetime import date

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models.projetos import Projetos, ContextoOrientacao, StatusProjeto

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

if __name__ == '__main__':
    pass