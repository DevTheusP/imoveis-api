from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)

def test_health_check_retorna_200_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Enterprise API is running"}

def test_listar_imoveis_status_code():
    response = client.get("/imoveis/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
