from typing import List

from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models.user import User
from backend.database.models.estudante import Estudante
from backend.database.models.professor import Professor
from backend.database.models.projetos import Projetos
from backend.database.models.universidade import Universidade
from backend.database.models.solicitacoes_projetos import SolicitacaoProjeto

from backend.database.models.site_schemas import DashboardAdmin, UsuarioModel, ProjetoModel, CandidaturaModel, PropostasModel, UniversidadeModel, AtualizarUserModel, ProfessorModel, EstudanteModel, UniversidadeDetalhadoModel

"""
GERAL
"""
def get_universidades() -> List[UniversidadeModel]:
    db: Session = SessionLocal()
    
    try:
        universidades = db.query(Universidade).all()
        
        return [UniversidadeModel(
            id=u.id,
            nome=u.nome,
            sigla=u.sigla,
            cidade=u.cidade,
            estado=u.estado
        ) for u in universidades]
    
    finally:
        db.close()

def get_universidades_detalhado() -> List[UniversidadeDetalhadoModel]:
    db: Session = SessionLocal()
        
    try:
        universidades = db.query(Universidade).all()
        
        return [UniversidadeDetalhadoModel(
            id=u.id,
            nome=u.nome,
            sigla=u.sigla,
            cidade=u.cidade,
            estado=u.estado,
            total_usuarios=db.query(Estudante).filter(Estudante.universidade_id==u.id).count() + db.query(Professor).filter(Professor.universidade_id==u.id).count()
        ) for u in universidades]
        
    finally:
        db.close()

def get_estudante_by_id(user_id: int) -> EstudanteModel:
    pass

def get_professor_by_id(user_id: int) -> ProfessorModel:
    pass

"""
ADMIN
"""
# TODO: Finalizar de colocar os dados
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
        usuarios_recentes = get_admin_users(10)
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

def get_admin_users(limit: int | None = None) -> List[UsuarioModel]:
    usuarios = []
    db: Session = SessionLocal()

    try:
        estudantes = db.query(Estudante).join(User).order_by(User.id.desc()).limit(limit).all()
        professores = db.query(Professor).join(User).order_by(User.id.desc()).limit(limit).all()

        for estudante in estudantes:
            user = estudante.user

            usuarios.append(
                UsuarioModel(
                    id=user.id,
                    nome=user.nome,
                    username=user.username,
                    email=user.email,
                    telegram_id=user.telegram_id,
                    role=user.role,
                    tipo="estudante",
                    universidade=estudante.universidade.nome if estudante.universidade else "",
                    universidade_sigla=estudante.universidade.sigla if estudante.universidade else "",
                    ativo=user.ativo
                )
            )

        for professor in professores:
            user = professor.user

            usuarios.append(
                UsuarioModel(
                    id=user.id,
                    nome=user.nome,
                    username=user.username,
                    email=user.email,
                    telegram_id=user.telegram_id,
                    role=user.role,
                    tipo="professor",
                    universidade=professor.universidade.nome if professor.universidade else "",
                    universidade_sigla=professor.universidade.sigla if professor.universidade else "",
                    ativo=user.ativo
                )
            )

        usuarios.sort(key=lambda usuario: usuario.id, reverse=True)

        return usuarios

    finally:
        db.close()

# TODO: Finalizar de colocar os dados (Cronograma, etc...)
def get_admin_projetos(limit: int | None = None, user_id: int | None = None) -> List[ProjetoModel]:
    db: Session = SessionLocal()
    
    try:
        estudante = db.query(Estudante).filter(Estudante.user_id==user_id).first()
        professor = db.query(Professor).filter(Professor.user_id==user_id).first()
        
        estudante_id = None
        professor_id = None
        universidade = None
        
        if estudante:
            estudante_id = estudante.id
            universidade = estudante.universidade
        
        if professor:
            professor_id = professor.id
            universidade = professor.universidade
            
        projetos = db.query(Projetos).filter(Projetos.estudante_id==estudante_id, Projetos.professor_id==professor_id).limit(limit).all()
        
        universidade=UniversidadeModel(
            id=universidade.id,
            nome=universidade.nome,
            sigla=universidade.sigla,
            cidade=universidade.cidade,
            estado=universidade.estado
        )
        
        
        if estudante:
            estudante=get_estudante_by_id(estudante_id)
            
            return [ProjetoModel(
                id=projeto.id,
                titulo=projeto.titulo,
                descricao=projeto.descricao,
                status=projeto.status,
                contexto=projeto.contexto,
                data_inicio=projeto.data_inicio,
                data_fim=projeto.data_fim,
                palavras_chave=projeto.palavras_chave,
                universidade=universidade,
                estudante=estudante,
                professor=get_professor_by_id(projeto.professor_id)
                ) for projeto in projetos]
        elif professor:
            professor=get_professor_by_id(professor_id)
                        
            return [ProjetoModel(
                id=projeto.id,
                titulo=projeto.titulo,
                descricao=projeto.descricao,
                status=projeto.status,
                contexto=projeto.contexto,
                data_inicio=projeto.data_inicio,
                data_fim=projeto.data_fim,
                palavras_chave=projeto.palavras_chave,
                universidade=universidade,
                professor=professor,
                estudante=get_estudante_by_id(projeto.estudante_id)
                ) for projeto in projetos]
        
        return [ProjetoModel(
            id=projeto.id,
            titulo=projeto.titulo,
            descricao=projeto.descricao,
            status=projeto.status,
            contexto=projeto.contexto,
            data_inicio=projeto.data_inicio,
            data_fim=projeto.data_fim,
            palavras_chave=projeto.palavras_chave,
            universidade=universidade,
            professor=get_professor_by_id(projeto.professor_id),
            estudante=get_estudante_by_id(projeto.estudante_id)
            ) for projeto in projetos]
    
    finally:
        db.close()

def get_admin_candidaturas() -> List[CandidaturaModel]:
    pass

def get_admin_propostas() -> List[PropostasModel]:
    pass

def get_admin_user_data(user_id: int) -> AtualizarUserModel | None:
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        estudante = db.query(Estudante).filter(Estudante.user_id == user.id).first()
        professor = db.query(Professor).filter(Professor.user_id == user.id).first()

        universidade = None

        if estudante and estudante.universidade:
            universidade = estudante.universidade

        elif professor and professor.universidade:
            universidade = professor.universidade

        usuario_model = UsuarioModel(
            id=user.id,
            nome=user.nome,
            username=user.username,
            email=user.email,
            telegram_id=user.telegram_id,
            role=user.role,
            tipo="estudante" if estudante else "professor" if professor else user.role,
            universidade=universidade.nome if universidade else "",
            universidade_sigla=universidade.sigla if universidade else "",
            ativo=user.ativo
        )
        
        universidade=UniversidadeModel(
            id=universidade.id,
            nome=universidade.nome,
            sigla=universidade.sigla,
            cidade=universidade.cidade,
            estado=universidade.estado
        )

        estudante_model = None

        if estudante:
            estudante_model = EstudanteModel(
                id=estudante.id,
                nome=user.nome,
                username=user.username,
                matricula=estudante.matricula,
                curso=estudante.curso,
                periodo=estudante.periodo,
                lattes=estudante.lattes,
                previsao_conclusao=estudante.previsao_conclusao,
                universidade=universidade
            )

        professor_model = None

        if professor:
            professor_model = ProfessorModel(
                id=professor.id,
                nome=user.nome,
                username=user.username,
                departamento=professor.departamento,
                area_pesquisa=professor.area_pesquisa,
                sala=professor.sala,
                universidade=universidade,
                lattes=professor.lattes
            )
            
        return AtualizarUserModel(
            usuario=usuario_model,
            estudante=estudante_model,
            professor=professor_model,
            tipo="estudante" if estudante else "professor" if professor else user.role,
            universidade=universidade
        )

    finally:
        db.close()

if __name__ == '__main__':
    pass