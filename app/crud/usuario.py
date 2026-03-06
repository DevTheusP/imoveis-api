from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import gerar_hash_senha

def get_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def criar_usuario(db: Session, usuario: UsuarioCreate):
    # Transforma a senha "123456" em um hash seguro "$2b$12$..."
    senha_hash = gerar_hash_senha(usuario.senha)
    
    db_usuario = Usuario(
        email=usuario.email,
        senha_hash=senha_hash
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
