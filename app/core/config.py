from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic vai tentar ler essas variáveis do arquivo .env primeiro
    PROJECT_NAME: str = "Imóveis Enterprise"
    PROJECT_VERSION: str = "2.0.0"
    
    # URL do banco com um valor padrão caso não exista no .env
    DATABASE_URL: str = "sqlite:///./imoveis.db"

    SECRET_KEY: str = "chave-padrao-caso-nao-tenha-no-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # Configuração para ler o arquivo .env
    model_config = SettingsConfigDict(env_file=".env")

# Instância global para ser usada em todo o projeto
settings = Settings()
