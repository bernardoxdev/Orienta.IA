from typing import Optional

from pydantic import BaseModel, ConfigDict

class Status(BaseModel):
    status: str
    
class StatusResponse(BaseModel):
    success: bool = True
    status: str
    
class LoginAndRegister(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class Refresh(BaseModel):
    access_token: str
    token_type: str

class UserVerification(BaseModel):
    id: Optional[int] = None
    nome: str
    username: str
    email: str
    telegram_id: Optional[str]
    senha: str
    role: str
    tipo: Optional[str]
    ativo: Optional[bool]
    universidade_id: Optional[int]
    
    matricula: Optional[str]
    curso: Optional[str]
    periodo: Optional[str]
    lattes: Optional[str]
    previsao_conclusao: Optional[str]
    
    departamento: Optional[str]
    area_pesquisa: Optional[str]
    sala: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)