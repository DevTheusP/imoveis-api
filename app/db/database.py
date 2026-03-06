from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# url de conexão com o sqlite vai criar um arquivo chamado imoveis.db na mesma pasta

SQLALCHEMY_DATABASE_URL = "sqlite:///./imoveis.db"

# engine é quem conversa com o banco
# check_same_thread=False é para o sqlite quando usado com o fastapi ( que é assíncrono) não bloquear a thread
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# sessionlocal é a nossa sessao , usada para fazer as queries
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para que as tabelas herdem as propriedades do sqlalchemy
Base = declarative_base()

# Dependencia do fastapi: toda vez que uma rota precisar do banco ela chama essa função
# pega a sessao, faz o que tenque fazer e no finally garante que vai fechar a sessao

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


