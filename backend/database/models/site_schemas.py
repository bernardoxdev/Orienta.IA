from pydantic import BaseModel, Field, ConfigDict

from typing import Optional, List

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
    id: Optional[int] = None
    nome: str
    sigla: str
    cidade: str
    estado: str
    
    model_config = ConfigDict(from_attributes=True)

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

class ConfiguracoesModel(BaseModel):
    nome_plataforma: str = "Orienta.IA"
    descricao: str = "Plataforma para conectar estudantes, professores e oportunidades acadêmicas"
    email_administrativo: str = "bernardocmfgomes@gmail.com"
    permitir_cadastro: bool = True
    aprovar_cadastro: bool = False
    permitir_telegram: bool = True
    permitir_projetos: bool = True
    permitir_candidaturas: bool = True
    permitir_propostas: bool = True
    notificacoes_email: bool = True
    notificacoes_sistema: bool = True
    tempo_sessao: int = 60
    tentativas_login: int = 5
    modo_manutencao: bool = False
    
    model_config = ConfigDict(from_attributes=True)

class DadosAdminModel(BaseModel):
    total_registros: int
    usuarios: int
    estudantes: int
    professores: int
    universidades: int
    projetos: int
    cronogramas: int
    solicitacoes_projeto: int
    solicitacoes_cancelamento: int
    solicitacoes_vincular: int
    ultima_verificacao: str
    status_banco: str
    
    model_config = ConfigDict(from_attributes=True)

class NotificacoesAdminModel(BaseModel):
    id: int
    titulo: str
    mensagem: str
    tipo: str
    destinatario: str
    destinatarios: int
    data: str
    lida: bool
    status: str
    icone: str
    
    model_config = ConfigDict(from_attributes=True)

class EstatisticasNotificacoesAdminModel(BaseModel):
    total: int
    nao_lidas: int
    enviadas: int
    pendentes: int
    
class ConversasIconsModel(BaseModel):
    id: int
    usuario_id: int
    nome: str
    username: str
    tipo: str
    iniciais: str
    assunto: str
    ultima_mensagem: str
    data: str
    nao_lidas: int
    online: bool

class MensagemModel(BaseModel):
    id: int
    remetente: str
    iniciais: str
    mensagem: str
    data: str
    propria: bool

if __name__ == '__main__':
    pass