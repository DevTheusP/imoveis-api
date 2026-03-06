from fastapi.testclient import TestClient
from main import app

# cria um cliente de teste que finge ser um usuario fazendo requisicoes
client = TestClient(app)

def test_health_check_retorna_200_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Imoveis API is running"}