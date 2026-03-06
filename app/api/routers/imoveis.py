from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.imovel import ImovelCreate, ImovelResponse
from app.crud import imovel as crud_imovel # Importa o crud

# Cria o router. O 'prefix' evita que a gente tenha que digitar '/imoveis' em cada rota.
router = APIRouter(prefix="/imoveis", tags=["Imóveis"])

@router.post("/", response_model=ImovelResponse)
def create_imovel(imovel: ImovelCreate, db: Session = Depends(get_db)):
    """
    Cria um novo imóvel.
    """
    return crud_imovel.create_imovel(db=db, imovel=imovel)

@router.get("/", response_model=List[ImovelResponse])
def read_imoveis(db: Session = Depends(get_db)):
    """
    Lista todos os imóveis.
    """
    return crud_imovel.get_imoveis(db=db)
