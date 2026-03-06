from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.database import Base 

class Imovel(Base):
    __tablename__ = "imoveis"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, nullable=True)
    preco = Column(Float)
    quartos = Column(Integer)
    banheiros = Column(Integer)
    vagas_garagem = Column(Integer, default=0)
    vendido = Column(Boolean, default=False)
