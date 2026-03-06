from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

# o sqlalchemy vai ler essa classe e criar a tabela no banco de dados

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
    
    
    