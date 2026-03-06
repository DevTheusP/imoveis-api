from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models 
from database import engine
from pydantic import BaseModel, ConfigDict
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db

# cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

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

# schemas pydantic (validacao entrada e saida)
class ImovelCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    preco: float
    quartos: int
    banheiros: int
    vagas_garagem: int = 0
class ImovelResponse(ImovelCreate):
    id: int
    vendido: bool
    
    model_config = ConfigDict(from_attributes=True)
    


@app.post("/imoveis", tags=["Imoveis"], response_model=ImovelResponse)
async def create_imovel(imovel: ImovelCreate, db: Session = Depends(get_db)):
    # cria um imovel no banco de dados
    # retorna o imovel criado
    db_imovel = models.Imovel(**imovel.model_dump())
    db.add(db_imovel)
    db.commit()
    db.refresh(db_imovel)
    return db_imovel

@app.get("/imoveis", tags=["Imoveis"], response_model=list[ImovelResponse])
async def list_imoveis(db: Session = Depends(get_db)):
    # lista todos os imoveis do banco de dados
    # retorna uma lista de imoveis
    imoveis = db.query(models.Imovel).all()
    return imoveis

#  health check
@app.get("/health", tags=["Health"])
async def health_check():
    # retorna um json com status ok e mensagem
    # útil para verificar se a api está funcionando
    # principalmente para os load balancers
    return {"status": "ok",
    "message": "Imoveis API is running"}