from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.config import settings
from app.crud import usuario as crud_usuario
from app.models.usuario import Usuario

# Define onde a API deve procurar o Token (na rota /login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_usuario_atual(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    usuario = crud_usuario.get_usuario_por_email(db, email=email)
    if usuario is None:
        raise credentials_exception
    return usuario
