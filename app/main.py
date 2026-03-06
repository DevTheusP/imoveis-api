from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.models import imovel as models_imovel
from app.api.routers import imoveis

# Criação das tabelas (No mundo real, usa o Alembic para migrações,
# mas aqui mantemos o create_all para simplicidade do MVP).
models_imovel.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Imóveis API - Enterprise Version",
    description="API modularizada seguindo padrões corporativos de arquitetura.",
    version="2.0.0"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas do arquivo imoveis.py
app.include_router(imoveis.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Enterprise API is running"}
