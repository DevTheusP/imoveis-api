import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
from app.core.config import settings

# Chave secreta para assinar o Token 
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def verificar_senha(senha_puro: str, hashed_password: str) -> bool:
    # O bcrypt espera bytes, então convertemos a string
    return bcrypt.checkpw(senha_puro.encode('utf-8'), hashed_password.encode('utf-8'))

def gerar_hash_senha(senha: str) -> str:
    # Gera um salt e o hash. O retorno do bcrypt é bytes, convertemos de volta para string
    salt = bcrypt.gensalt()
    pwd_bytes = senha.encode('utf-8')
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
