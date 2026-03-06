from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.db.database import engine
from app.models import imovel as models_imovel
from app.models import usuario as models_usuario # <--- Novo modelo
from app.api.routers import imoveis, auth
from app.core.config import settings # <--- Faltava este import!

# Criação das tabelas
models_imovel.Base.metadata.create_all(bind=engine)
models_usuario.Base.metadata.create_all(bind=engine) # <--- Cria tabela de usuários

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API modularizada seguindo padrões corporativos de arquitetura.",
    version=settings.PROJECT_VERSION,
)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Opa! Ocorreu um erro interno no servidor.", "detail": str(exc)},
    )

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(auth.router) # <--- Rotas de Login/Cadastro
app.include_router(imoveis.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Enterprise API is running"}
