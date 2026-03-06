from pydantic import BaseModel, EmailStr, ConfigDict

# O que recebemos na hora do cadastro
class UsuarioCreate(BaseModel):
    email: EmailStr # Isso valida se o texto é um email real (ex: fulano@email.com)
    senha: str

# O que respondemos (sem a senha)
class UsuarioResponse(BaseModel):
    id: int
    email: EmailStr
    esta_ativo: bool

    model_config = ConfigDict(from_attributes=True)

# Estrutura do Token que devolve no login
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
