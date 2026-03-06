from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

# 1. Health Check (Continua igual)
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

# Helper para pegar o token nos outros testes
def obter_token_teste():
    # Cadastra um usuário de teste
    email_teste = "testador@email.com"
    senha_teste = "senha123"
    
    # Garante que o usuário existe
    client.post("/usuarios", json={"email": email_teste, "senha": senha_teste})
    
    # Faz o login para pegar o token
    response = client.post(
        "/login", 
        data={"username": email_teste, "password": senha_teste}
    )
    return response.json()["access_token"]

# 3. Teste de Rota Protegida (Tentar criar sem token deve falhar)
def test_criar_imovel_sem_token_falha():
    response = client.post("/imoveis/", json={
        "titulo": "Casa de Teste",
        "preco": 500000,
        "quartos": 3,
        "banheiros": 2
    })
    assert response.status_code == 401 # Unauthorized

# 4. Teste de Rota Protegida (Com token deve funcionar)
def test_criar_imovel_com_token_sucesso():
    # Pega o token usando o helper
    token = obter_token_teste()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/imoveis/", headers=headers, json={
        "titulo": "Mansão de Teste",
        "preco": 1500000,
        "quartos": 5,
        "banheiros": 4,
        "vagas_garagem": 3
    })
    
    assert response.status_code == 200
    assert response.json()["titulo"] == "Mansão de Teste"
