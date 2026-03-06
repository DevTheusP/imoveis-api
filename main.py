from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# inicializa o fastapi com metadados pro swagger (/docs)
app = FastAPI(
    title="imoveis api", # titulo do swagger
    description="API para gerenciar imoveis.", # descrição do swagger
    version="1.0.0", # versão do swagger
)

# configuração cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # permite requisições de qualquer origem, em producao é só o domínio do frontend
    allow_credentials=True,
    allow_methods=["*"], # permite requisições de qualquer método
    allow_headers=["*"], # permite requisições de qualquer header
)


#  health check
@app.get("/health", tags=["Health"])
async def health_check():
    # retorna um json com status ok e mensagem
    # útil para verificar se a api está funcionando
    # principalmente para os load balancers
    return {"status": "ok",
    "message": "Imoveis API is running"}