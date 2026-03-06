from pydantic import BaseModel, ConfigDict
from typing import Optional

# O que é necessário para criar um imóvel
class ImovelCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    preco: float
    quartos: int
    banheiros: int
    vagas_garagem: int = 0

# Como o imóvel é retornado (já com ID e status)
class ImovelResponse(ImovelCreate):
    id: int
    vendido: bool

    model_config = ConfigDict(from_attributes=True)
