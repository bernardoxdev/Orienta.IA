from typing import List

from sqlalchemy.orm import Session, joinedload

from backend.database.connection import SessionLocal
from backend.database.models.user import User
from backend.database.models.estudante import Estudante
from backend.database.models.professor import Professor
from backend.database.models.projetos import Projetos
from backend.database.models.solicitacoes_projetos import SolicitacaoProjeto

from backend.database.models.site_schemas import DashboardAdmin, UsuarioModel, ProjetoModel, CandidaturaModel, PropostasModel

"""
ADMIN
"""
def get_dashboard_admin_data() -> DashboardAdmin:
    db: Session = SessionLocal()
    
    try:
        total_usuarios = db.query(User).count()
        total_estudantes = db.query(Estudante).count()
        total_professores = db.query(Professor).count()
        total_projetos = db.query(Projetos).count()
        total_candidaturas = 0  # TODO: Quem se candidata a projetos
        candidaturas_pendentes = 0 # TODO: Quem se candidata a projetos
        propostas_pendentes = db.query(SolicitacaoProjeto).count()
        mensagens_pendentes = 0 # TODO: Implementar contagem de mensagens pendentes
        notificacoes_nao_lidas = 0  # TODO: Implementar contagem de notificações não lidas
        usuarios_recentes = []  # Pegar 10 usuarios do menos recentes
        atividades = []  # Pegar 10 atividades recentes
        notificacoes = []  # TODO: Finalizar sistema de notificações -> Pegar últimas 5 notificações

        return DashboardAdmin(
            total_usuarios=total_usuarios,
            total_estudantes=total_estudantes,
            total_professores=total_professores,
            total_projetos=total_projetos,
            total_candidaturas=total_candidaturas,
            candidaturas_pendentes=candidaturas_pendentes,
            propostas_pendentes=propostas_pendentes,
            mensagens_pendentes=mensagens_pendentes,
            notificacoes_nao_lidas=notificacoes_nao_lidas,
            usuarios_recentes=usuarios_recentes,
            atividades=atividades,
            notificacoes=notificacoes
        )
        
    finally:
        db.close()

def get_admin_users() -> List[UsuarioModel]:
    db: Session = SessionLocal()

    try:
        users = db.query(User).options(joinedload(User.estudantes).joinedload(Estudante.universidade), joinedload(User.professores).joinedload(Professor.universidade)).all()
        usuarios = []

        for user in users:
            tipo = "usuario"
            universidade = ""
            universidade_sigla = ""

            if user.estudante:
                tipo = "estudante"

                universidade = user.estudante.universidade.nome if user.estudante.universidade else ""
                universidade_sigla = user.estudante.universidade.sigla if user.estudante.universidade else ""

            elif user.professor:
                tipo = "professor"

                universidade = user.professor.universidade.nome if user.professor.universidade else ""
                universidade_sigla = user.professor.universidade.sigla if user.professor.universidade else ""

            usuarios.append(
                UsuarioModel(
                    id=user.id,
                    nome=user.nome,
                    username=user.username,
                    email=user.email,
                    telegram_id=user.telegram_id,
                    role=user.role,
                    tipo=tipo,
                    universidade=universidade,
                    universidade_sigla=universidade_sigla,
                    ativo=user.ativo
                )
            )

        return usuarios

    finally:
        db.close()

def get_admin_projetos() -> List[ProjetoModel]:
    pass

def get_admin_candidaturas() -> List[CandidaturaModel]:
    pass

def get_admin_propostas() -> List[PropostasModel]:
    pass

if __name__ == '__main__':
    pass