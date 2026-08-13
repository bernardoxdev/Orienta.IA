from pydantic import BaseModel, Field

from typing import Optional

from backend.database.models.projetos import StatusProjeto, ContextoOrientacao

class DashboardAdmin(BaseModel):
    total_usuarios: int = 0
    total_estudantes: int = 0
    total_professores: int = 0
    total_projetos: int = 0
    total_candidaturas: int = 0
    candidaturas_pendentes: int = 0
    propostas_pendentes: int = 0
    mensagens_pendentes: int = 0
    notificacoes_nao_lidas: int = 0
    usuarios_recentes: list = Field(default_factory=list)
    atividades: list = Field(default_factory=list)
    notificacoes: list = Field(default_factory=list)

class UsuarioModel(BaseModel):
    id: int
    nome: str
    username: str
    email: str
    telegram_id: Optional[str]
    role: str
    tipo: str
    universidade: str
    universidade_sigla: str
    ativo: bool

class DashboardAdminSideModel(BaseModel):
    candidaturas_pendentes: int = 0
    propostas_pendentes: int = 0
    mensagens_pendentes: int = 0
    notificacoes_nao_lidas: int = 0

    
class UniversidadeModel(BaseModel):
    id: int
    nome: str
    sigla: str
    cidade: str
    estado: str

class UniversidadeDetalhadoModel(BaseModel):
    id: int
    nome: str
    sigla: str
    cidade: str
    estado: str
    total_usuarios: int = 0

class ProfessorModel(BaseModel):
    id: int
    nome: str
    username: str
    departamento: str
    area_pesquisa: str
    sala: str
    universidade: UniversidadeModel
    lattes: Optional[str]
    
class EstudanteModel(BaseModel):
    id: int
    nome: str
    username: str
    matricula: str
    curso: str
    periodo: int
    lattes: Optional[str]
    previsao_conclusao: str
    universidade: UniversidadeModel

class ProjetoModel(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: StatusProjeto
    contexto: ContextoOrientacao
    data_inicio: Optional[str]
    data_fim: Optional[str]
    palavras_chave: list
    cronogramas_total: Optional[int]
    cronogramas_concluidos: Optional[int]
    estudante: EstudanteModel
    professor: ProfessorModel
    universidade: UniversidadeModel

class CandidaturaModel(BaseModel):
    id: int
    tipo: str
    status: str
    estudante: EstudanteModel
    projeto: ProjetoModel
    professor: ProfessorModel
    universidade: UniversidadeModel
    data: str
    mensagem: Optional[str]

class PropostasModel(BaseModel):
    id: int
    titulo: str
    descricao: str
    estudante: EstudanteModel
    universidade: UniversidadeModel
    contexto: str
    area: str
    palavras_chave: list
    status: str
    data: str
    observacoes: Optional[str]

class AtualizarUserModel(BaseModel):
    usuario: UsuarioModel
    estudante: EstudanteModel | None = None
    professor: ProfessorModel | None = None
    tipo: str
    universidade: UniversidadeModel | None = None

if __name__ == '__main__':
    pass