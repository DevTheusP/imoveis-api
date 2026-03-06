from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.core import security
from app.core.config import settings
from app.crud import usuario as crud_usuario
from app.schemas import usuario as schema_usuario

router = APIRouter(tags=["Autenticação"])

@router.post("/usuarios", response_model=schema_usuario.UsuarioResponse)
def cadastrar_usuario(usuario: schema_usuario.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud_usuario.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return crud_usuario.criar_usuario(db=db, usuario=usuario)

@router.post("/login", response_model=schema_usuario.Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # O OAuth2PasswordRequestForm espera 'username' (que será o nosso email) e 'password'
    usuario = crud_usuario.get_usuario_por_email(db, email=form_data.username)
    if not usuario or not security.verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.criar_token_acesso(
        data={"sub": usuario.email}, expires_delta=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
