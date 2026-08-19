from typing import List, Optional

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal

from backend.database.models.site_schemas import UniversidadeModel
from backend.database.models.return_schemas import StatusResponse

from backend.database.models.universidade import Universidade
from backend.database.models.professor import Professor
from backend.database.models.estudante import Estudante

async def get_universidade_by_nome_ou_sigla(texto: str) -> Optional[Universidade]:
    db = SessionLocal()

    try:
        universidade = (
            db.query(Universidade)
            .filter(
                (Universidade.nome.ilike(texto)) |
                (Universidade.sigla.ilike(texto))
            )
            .first()
        )

        return universidade
    finally:
        db.close()

async def get_universidades() -> List[Universidade]:
    db = SessionLocal()

    try:
        universidades = db.query(Universidade).all()
        return universidades
    finally:
        db.close()

async def get_universidade_nome_by_id(universidade_id: int) -> Optional[str]:
    db = SessionLocal()

    try:
        universidade = db.query(Universidade).filter(Universidade.id == universidade_id).first()
        if universidade:
            return universidade.nome
        return None
    finally:
        db.close()
        
def deletar_universidade_by_id(universidade_id: int) -> StatusResponse:
    db: Session = SessionLocal()

    try:
        universidade = db.query(Universidade).filter(Universidade.id == universidade_id).first()

        if not universidade:
            return False, "Universidade não encontrada."

        estudantes = db.query(Estudante).filter(Estudante.universidade_id == universidade_id).count()

        professores = db.query(Professor).filter(Professor.universidade_id == universidade_id).count()

        if estudantes > 0 or professores > 0:
            return StatusResponse(
                success=False,
                status=f"Não é possível excluir esta universidade. Existem {estudantes} estudante(s) e {professores} professor(es) vinculados."
            )

        db.delete(universidade)
        db.commit()

        return StatusResponse(
            success=True,
            status="Universidade excluída com sucesso."
        )

    except Exception as e:
        db.rollback()
        return StatusResponse(
            success=False,
            status=f"Erro ao excluir universidade: {str(e)}"
        )

    finally:
        db.close()

def atualizar_dados_universidade(universidade: UniversidadeModel) -> Optional[UniversidadeModel]:
    db: Session = SessionLocal()

    try:
        universidade_db = db.query(Universidade).filter(Universidade.id == universidade.id).first()

        if not universidade_db:
            return None

        universidade_db.nome = universidade.nome
        universidade_db.sigla = universidade.sigla
        universidade_db.cidade = universidade.cidade
        universidade_db.estado = universidade.estado

        db.commit()
        db.refresh(universidade_db)

        return UniversidadeModel.model_validate(universidade_db)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def criar_universidade(universidade: UniversidadeModel) -> UniversidadeModel:
    db: Session = SessionLocal()

    try:
        nova_universidade = Universidade(
            nome=universidade.nome,
            sigla=universidade.sigla,
            cidade=universidade.cidade,
            estado=universidade.estado
        )

        db.add(nova_universidade)
        db.commit()
        db.refresh(nova_universidade)

        return UniversidadeModel.model_validate(nova_universidade)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
        
if __name__ == '__main__':
    pass