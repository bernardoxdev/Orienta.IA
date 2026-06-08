from pydantic import BaseModel

class LoginRequest(BaseModel):
    dadoLogin: str
    password: str

class RegisterRequest(BaseModel):
    nome: str
    username: str
    email: str
    password: str
    
class RegisterAdminRequest(BaseModel):
    nome: str
    username: str
    email: str
    password: str
    role: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class RefreshRequest(BaseModel):
    refresh_token: str