from pydantic import BaseModel, Field

from typing import Optional

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

class ProfessorModel(BaseModel):
    id: int
    nome: str
    username: str
    
class EstudanteModel(BaseModel):
    id: int
    nome: str
    username: str
    matricula: str

class UniversidadeModel(BaseModel):
    id: int
    nome: str
    sigla: str

class ProjetoModel(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: str
    contexto: str
    data_inicio: str
    data_fim: str
    cronogramas_total: int
    cronogramas_concluidos: int
    palavras_chave: list
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

if __name__ == '__main__':
    pass