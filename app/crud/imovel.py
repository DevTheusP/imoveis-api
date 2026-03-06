from sqlalchemy.orm import Session
from app.models.imovel import Imovel
from app.schemas.imovel import ImovelCreate

# Função para buscar todos os imóveis (equivalente ao SELECT * FROM imoveis)
def get_imoveis(db: Session):
    return db.query(Imovel).all()

# Função para criar um novo imóvel (equivalente ao INSERT INTO)
def create_imovel(db: Session, imovel: ImovelCreate):
    db_imovel = Imovel(**imovel.model_dump())
    db.add(db_imovel)
    db.commit()
    db.refresh(db_imovel)
    return db_imovel
